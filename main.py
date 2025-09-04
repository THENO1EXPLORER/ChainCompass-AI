import requests
import json
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI(title="ChainCompass API")

def parse_quote(quote_data):
    """
    This function takes the full JSON response and extracts the important details.
    """
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

# Define your first API endpoint at the root URL ("/")
@app.get("/")
def read_root():
    return {"message": "Welcome to the ChainCompass API!"}

# This is the new endpoint for getting a quote
@app.get("/api/v1/quote")
def get_lifi_quote(fromChain: str, toChain: str, fromToken: str, toToken: str, fromAmount: str):
    """
    Takes swap details as input, fetches the best quote from LI.FI,
    parses it, and returns a clean summary.
    """
    params = {
        "fromChain": fromChain,
        "toChain": toChain,
        "fromToken": fromToken,
        "toToken": toToken,
        "fromAmount": fromAmount,
        "fromAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" # Using our placeholder
    }
    api_url = "https://li.quest/v1/quote"

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        raw_quote_data = response.json()
        clean_summary = parse_quote(raw_quote_data)
        return clean_summary

    except requests.exceptions.HTTPError as err:
        return {"error": "Failed to fetch quote from LI.FI", "details": err.response.text}
    except Exception as err:
        return {"error": "An unexpected error occurred", "details": str(err)}