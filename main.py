import requests
import json
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables (for OpenAI API key)
load_dotenv()

# Create an instance of the FastAPI class
app = FastAPI(title="ChainCompass API")

# --- (Your parse_quote function stays here, unchanged) ---
def parse_quote(quote_data):
    # ... (same as before)
    estimate = quote_data.get("estimate", {})
    tool_details = quote_data.get("toolDetails", {})
    provider_name = tool_details.get("name", "N/A")
    execution_time_seconds = estimate.get("executionDuration", 0)
    final_output_usd = estimate.get("toAmountUSD", "0")
    total_fees_usd = 0
    for fee in estimate.get("feeCosts", []):
        total_fees_usd += float(fee.get("amountUSD", 0))
    summary = {
        "provider": provider_name,
        "time_seconds": execution_time_seconds,
        "fees_usd": total_fees_usd,
        "output_usd": float(final_output_usd)
    }
    return summary

# --- Initialize LangChain components ---
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template(
    "You are a helpful crypto assistant called ChainCompass. "
    "Summarize the following best route for a user in a friendly, single sentence. "
    "Mention the provider, the estimated time, the final amount in USD, and the fees. "
    "Route details: Provider={provider}, Time={time_seconds}s, Fees of approximately ${fees_usd:.2f} USD, resulting in a final amount of ${output_usd:.2f} USD."
)
chain = prompt | llm

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the ChainCompass API!"}

@app.get("/api/v1/quote")
def get_lifi_quote(fromChain: str, toChain: str, fromToken: str, toToken: str, fromAmount: str):
    params = { "fromChain": fromChain, "toChain": toChain, "fromToken": fromToken, "toToken": toToken, "fromAmount": fromAmount, "fromAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" }
    api_url = "https://li.quest/v1/quote"

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        # 1. Get raw data
        raw_quote_data = response.json()

        # 2. Parse into clean summary
        clean_summary = parse_quote(raw_quote_data)

        # 3. NEW: Generate AI summary
        ai_response = chain.invoke(clean_summary)
        ai_summary = ai_response.content

        # 4. Return the AI's sentence
        return {"summary": ai_summary}

    except Exception as err:
        return {"error": "An error occurred", "details": str(err)}