import json

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

# --- Main part of the test script ---

# Load the data from your saved file instead of calling the API
with open('sample_response.json', 'r') as f:
    print("📄 Loading data from local sample file...")
    data = json.load(f)

# Test your parsing function with the local data
summary = parse_quote(data)

# Print the clean results
print("\n--- Quote Summary ---")
print(f"Provider: {summary['provider']}")
print(f"Est. Time: {summary['time_seconds']} seconds")
print(f"Total Fees: ${summary['fees_usd']:.2f}")
print(f"Est. Received: ${summary['output_usd']:.2f}")