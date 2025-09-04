import os
import requests
from dotenv import load_dotenv
import json

# This line loads the variables from your .env file
load_dotenv()

# --- 1. Define the Request Parameters ---
# These are the details of the quote we want to get
params = {
    "fromChain": "POL",      # The chain you are sending from (Polygon)
    "toChain": "ARB",        # The chain you are sending to (Arbitrum)
    "fromToken": "USDC",     # The token you are sending
    "toToken": "ETH",        # The token you want to receive
    "fromAmount": "100000000", # The amount (100 USDC, which has 6 decimals)
    "fromAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" # A real, valid placeholder address
}

# --- 2. Define the API URL ---
# The correct, official endpoint for getting a quote
api_url = "https://li.quest/v1/quote"  # Change this line in test_api.py
#api_url = "https://li.quest/v1/advanced/routes"

# --- 3. Make the API Request ---
print("🚀 Sending request to LI.FI API...")

try:
    # Send a GET request with our parameters
    response = requests.get(api_url, params=params)

    # This line will raise an error if the response was not successful (e.g., 400, 404, 500)
    response.raise_for_status()

    # If the request was successful, get the JSON data from the response
    quote_data = response.json()

    # --- 4. Handle the Successful Response ---
    print("✅ Successfully received a quote!")
    
    # Pretty-print the JSON response so it's easy to read
    print(json.dumps(quote_data, indent=4))

except requests.exceptions.HTTPError as err:
    # This block will run if the server returned an error (like 400 Bad Request)
    print(f"❌ HTTP Error: {err}")
    print(f"Server Response: {err.response.text}") # Print the detailed error message from the server
except Exception as err:
    # This block will run for any other errors (like a network issue)
    print(f"❌ An other error occurred: {err}")