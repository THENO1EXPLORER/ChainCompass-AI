import os
import json
import asyncio
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import SecretStr, BaseModel, Field
from cachetools import TTLCache
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential, retry_if_exception_type

# --- 1. Load and Validate Environment Variables ---
# This loads the .env file at the start of the application.
load_dotenv()

# We immediately get the API keys from the environment.
LIFI_API_KEY = os.getenv("LIFI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# This is a critical check. If the keys are not found, the server will stop
# with a clear error message. This prevents it from running in a broken state.
if not LIFI_API_KEY or not OPENAI_API_KEY:
    raise ValueError("CRITICAL ERROR: Make sure LIFI_API_KEY and OPENAI_API_KEY are set in your .env file or environment.")

print("✅ API keys and environment variables loaded successfully.")


# --- 2. Initialize Application and AI Components ---

# Create an instance of the FastAPI class, which is our backend server.
app = FastAPI(title="ChainCompass API")

# Enable CORS for local dev and deployed frontend
allowed_origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "https://chaincompass-ai-theno1explorer.streamlit.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Enable gzip compression for faster responses
app.add_middleware(GZipMiddleware, minimum_size=500)

# Initialize the OpenAI model we want to use (gpt-4o-mini for speed and cost).
# We wrap the API key in SecretStr to resolve the type warning.
llm = ChatOpenAI(model="gpt-4o-mini", api_key=SecretStr(OPENAI_API_KEY))

# This is the prompt template for our AI. It defines the AI's persona and instructions.
# The fields in {curly_braces} will be filled in with data from the LI.FI quote.
prompt = ChatPromptTemplate.from_template(
    "You are a helpful crypto assistant called ChainCompass. "
    "Summarize the following best route for a user in a friendly, single sentence. "
    "Mention the provider, the estimated time, the final amount in USD, and the fees. "
    "Route details: Provider={provider}, Time={time_seconds}s, Fees of approximately ${fees_usd:.2f} USD, resulting in a final amount of ${output_usd:.2f} USD."
)

# This creates a "chain" that links the prompt and the AI model together.
# When we call this chain, the data flows from the prompt to the model automatically.
chain = prompt | llm


# --- 3. Helper Functions ---

def parse_quote(quote_data):
    """
    This function takes the large, complex JSON response from LI.FI
    and extracts only the key pieces of information we care about.
    """
    estimate = quote_data.get("estimate", {})
    tool_details = quote_data.get("toolDetails", {})
    provider_name = tool_details.get("name", "N/A")
    execution_time_seconds = estimate.get("executionDuration", 0)
    final_output_usd = estimate.get("toAmountUSD", "0")
    
    # Calculate the total fees by adding up all fee costs.
    total_fees_usd = 0
    for fee in estimate.get("feeCosts", []):
        total_fees_usd += float(fee.get("amountUSD", "0"))
        
    # Return a clean, simple dictionary with our extracted data.
    summary = {
        "provider": provider_name,
        "time_seconds": execution_time_seconds,
        "fees_usd": total_fees_usd,
        "output_usd": float(final_output_usd)
    }
    return summary


# --- 4. API Endpoints ---

@app.get("/")
def read_root():
    """A simple endpoint to confirm the server is running."""
    return {"message": "Welcome to the ChainCompass API!"}

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

# Shared HTTP client with connection pooling
async_client: Optional[httpx.AsyncClient] = None

@app.on_event("startup")
async def on_startup() -> None:
    global async_client
    async_client = httpx.AsyncClient(
        base_url="https://li.quest",
        timeout=httpx.Timeout(15.0, read=15.0, connect=10.0),
        headers={
            "accept": "application/json",
            "x-lifi-api-key": LIFI_API_KEY,
        },
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        transport=httpx.AsyncHTTPTransport(retries=0)
    )

@app.on_event("shutdown")
async def on_shutdown() -> None:
    global async_client
    if async_client is not None:
        await async_client.aclose()
        async_client = None

# In-memory TTL cache for quotes
quote_cache: TTLCache = TTLCache(maxsize=1000, ttl=60)

# Request/Response models
class QuoteRequest(BaseModel):
    fromChain: str = Field(..., min_length=2, max_length=10)
    toChain: str = Field(..., min_length=2, max_length=10)
    fromToken: str = Field(..., min_length=2, max_length=12)
    toToken: str = Field(..., min_length=2, max_length=12)
    fromAmount: str = Field(..., pattern=r"^\d{1,30}$")
    fromAddress: Optional[str] = Field(
        default="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    )

class QuoteSummary(BaseModel):
    summary: str
    provider: Optional[str] = None
    time_seconds: Optional[int] = None
    fees_usd: Optional[float] = None
    output_usd: Optional[float] = None

@app.get("/api/v1/quote", response_model=QuoteSummary)
async def get_lifi_quote(
    fromChain: str = Query(..., min_length=2, max_length=10),
    toChain: str = Query(..., min_length=2, max_length=10),
    fromToken: str = Query(..., min_length=2, max_length=12),
    toToken: str = Query(..., min_length=2, max_length=12),
    fromAmount: str = Query(..., pattern=r"^\d{1,30}$"),
    fromAddress: Optional[str] = Query("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
):
    """
    Fetch LI.FI quote (pooled async client + TTL cache + retries) and summarize via LLM.
    """
    global async_client
    if async_client is None:
        raise HTTPException(status_code=503, detail="HTTP client not ready")

    req = QuoteRequest(
        fromChain=fromChain,
        toChain=toChain,
        fromToken=fromToken,
        toToken=toToken,
        fromAmount=fromAmount,
        fromAddress=fromAddress,
    )

    cache_key = (req.fromChain, req.toChain, req.fromToken, req.toToken, req.fromAmount, req.fromAddress)

    if cache_key in quote_cache:
        raw_quote_data = quote_cache[cache_key]
    else:
        async def fetch() -> dict:
            resp = await async_client.get("/v1/quote", params=req.model_dump())
            resp.raise_for_status()
            return resp.json()

        try:
            async for attempt in AsyncRetrying(
                reraise=True,
                stop=stop_after_attempt(3),
                wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
                retry=retry_if_exception_type((httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError))
            ):
                with attempt:
                    raw_quote_data = await fetch()
            quote_cache[cache_key] = raw_quote_data
        except httpx.HTTPStatusError as err:
            detail = err.response.text if err.response is not None else str(err)
            status = err.response.status_code if err.response is not None else 502
            raise HTTPException(status_code=status, detail=f"LI.FI error: {detail}")
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError) as err:
            raise HTTPException(status_code=504, detail=f"Upstream timeout: {str(err)}")
        except Exception as err:
            raise HTTPException(status_code=502, detail=f"Upstream failure: {str(err)}")

    clean_summary = parse_quote(raw_quote_data)
    # Offload blocking LLM call to thread executor to avoid blocking event loop
    ai_response = await asyncio.get_event_loop().run_in_executor(None, chain.invoke, clean_summary)
    ai_summary = ai_response.content

    return QuoteSummary(
        summary=ai_summary,
        provider=clean_summary.get("provider"),
        time_seconds=clean_summary.get("time_seconds"),
        fees_usd=clean_summary.get("fees_usd"),
        output_usd=clean_summary.get("output_usd"),
    )

