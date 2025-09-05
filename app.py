import streamlit as st
import requests
import pandas as pd

# Set up the title and icon of the web page
st.set_page_config(page_title="ChainCompass AI", page_icon="🧭")
st.title("🧭 ChainCompass AI")
st.caption("Your smart guide for cross-chain swaps.")

# --- Create the input fields for the user ---
st.subheader("Enter Swap Details")
from_chain = st.text_input("From Chain (e.g., POL)", "POL")
to_chain = st.text_input("To Chain (e.g., ARB)", "ARB")
from_token = st.text_input("From Token (e.g., USDC)", "USDC")
to_token = st.text_input("To Token (e.g., ETH)", "ETH")
from_amount_display = st.number_input("Amount to Swap (e.g., 100)", value=100)

# --- The button to trigger the API call ---
if st.button("Find Best Route"):
    # Convert the user-friendly amount to the smallest unit for the API
    # We'll assume 6 decimals for USDC as our primary example
    from_amount = int(from_amount_display * 10**6)

    # Define the API endpoint of YOUR backend server
    api_url = "http://127.0.0.1:8000/api/v1/quote"

    # The parameters for your API, taken from the input fields
    params = {
        "fromChain": from_chain,
        "toChain": to_chain,
        "fromToken": from_token,
        "toToken": to_token,
        "fromAmount": str(from_amount)
    }

    # --- Call your own API and display the result ---
    with st.spinner("Searching for the best route... This may take a moment."):
        try:
            # Make the request to your FastAPI backend
            response = requests.get(api_url, params=params)
            response.raise_for_status() # Raise an error on a bad response
            
            result = response.json()

            st.subheader("🏆 Best Route Found!")

            if "error" in result:
                st.error(f"An error occurred: {result.get('details', 'Unknown error')}")
            else:
                # Display the results in a clean table format
                df = pd.DataFrame([result])
                df_display = df[['provider', 'output_usd', 'time_seconds', 'fees_usd']].rename(columns={
                    'provider': 'Provider',
                    'output_usd': 'Est. Received (USD)',
                    'time_seconds': 'Est. Time (Seconds)',
                    'fees_usd': 'Total Fees (USD)'
                })
                st.dataframe(df_display, hide_index=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend server. Make sure it's running. Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")