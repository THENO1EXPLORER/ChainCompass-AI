import os
import requests
import json
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import SecretStr

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

@app.get("/api/v1/quote")
def get_lifi_quote(fromChain: str, toChain: str, fromToken: str, toToken: str, fromAmount: str):
    """
    This is the main endpoint. It takes swap details from the Streamlit frontend,
    fetches the best quote from LI.FI, parses it, and returns an AI-generated summary.
    """
    params = {
        "fromChain": fromChain,
        "toChain": toChain,
        "fromToken": fromToken,
        "toToken": toToken,
        "fromAmount": fromAmount,
        "fromAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" # A placeholder address
    }
    api_url = "https://li.quest/v1/quote"
    
    # Headers are required for authentication with the LI.FI API.
    headers = {
        "accept": "application/json",
        "x-lifi-api-key": LIFI_API_KEY # Use the key we loaded
    }

    try:
        # Make the actual request to the LI.FI server.
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status() # This will raise an error if the request fails
        
        # The main logic pipeline:
        raw_quote_data = response.json()         # 1. Get raw data
        clean_summary = parse_quote(raw_quote_data) # 2. Parse it
        ai_response = chain.invoke(clean_summary)   # 3. Send to AI
        ai_summary = ai_response.content          # 4. Get AI's text back
        
        # Return the final summary to the Streamlit frontend.
        return {"summary": ai_summary}
        
    except requests.exceptions.HTTPError as err:
        # Handle errors from the LI.FI API specifically
        return {"error": "Failed to fetch quote from LI.FI", "details": err.response.text}
    except Exception as err:
        # Handle any other unexpected errors
        return {"error": "An unexpected error occurred", "details": str(err)}

