import streamlit as st
import requests
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="ChainCompass AI",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Sample Data for Dropdowns ---
CHAINS = {"Polygon": "POL", "Arbitrum": "ARB", "Ethereum": "ETH", "Optimism": "OPT", "Base": "BASE"}
TOKENS = {"USDC": "USDC", "Ethereum": "ETH", "Tether": "USDT", "Wrapped BTC": "WBTC"}

# --- UI Sidebar ---
with st.sidebar:
    # Use the corrected parameter and ensure there is only ONE image line
    st.image("logo.png", use_container_width=True)
    st.info("This app is a demo for the DoraHacks 'DeFiTimez Multichain Mayhem' Hackathon.")
    with st.expander("How It Works", expanded=False):
        st.markdown("""
        1.  **You** enter your desired swap details.
        2.  **Our Backend (FastAPI on Render)** calls the LI.FI API to find the best swap routes.
        3.  **An AI (GPT-4o mini via LangChain)** analyzes the best route.
        4.  **You** get a simple, human-friendly summary of the optimal choice.
        """)

# --- Main Page Content ---
st.title("🧭 ChainCompass AI")
st.caption("Your smart guide for finding the best cross-chain swap routes.")

st.subheader("Enter Swap Details")

# --- Input Fields using Columns for a cleaner layout ---
col1, col2 = st.columns(2)
with col1:
    from_chain_name = st.selectbox("From Chain", options=list(CHAINS.keys()))
    from_token_name = st.selectbox("Token to Swap", options=list(TOKENS.keys()))
with col2:
    to_chain_name = st.selectbox("To Chain", options=list(CHAINS.keys()), index=1)
    to_token_name = st.selectbox("Token to Receive", options=list(TOKENS.keys()), index=1)

from_amount_display = st.number_input(
    f"Amount of {from_token_name} to Swap",
    value=100.0,
    min_value=0.01,
    step=10.0,
    help="Enter the amount of the token you want to swap."
)

# --- The button to trigger the API call ---
if st.button("Find Best Route", type="primary", use_container_width=True):
    # Convert display names to API symbols (e.g., "Polygon" -> "POL")
    from_chain = CHAINS[from_chain_name]
    from_token = TOKENS[from_token_name]
    to_chain = CHAINS[to_chain_name]
    to_token = TOKENS[to_token_name]

    # Assume 6 decimals for USDC, 18 for others. A real app would need a more robust way to handle this.
    decimals = 6 if from_token == "USDC" else 18
    from_amount = int(from_amount_display * (10**decimals))

    # Define the API endpoint of your deployed backend server
    api_url = "https://chaincompass-ai-krishnav.onrender.com/api/v1/quote"

    params = {
        "fromChain": from_chain,
        "toChain": to_chain,
        "fromToken": from_token,
        "toToken": to_token,
        "fromAmount": str(from_amount)
    }

    with st.spinner("Asking the AI for the best route..."):
        try:
            response = requests.get(api_url, params=params, timeout=60) # Increased timeout for long requests
            response.raise_for_status()
            result = response.json()

            st.subheader("🏆 Your AI Recommendation")

            if "error" in result:
                st.error(f"An error occurred: {result.get('details', 'Unknown error')}")
            else:
                ai_summary = result.get("summary", "No summary available.")
                st.markdown(f"""
                <div style="padding: 1rem; border-radius: 0.5rem; background-color: #e6f7ff; border-left: 6px solid #1890ff;">
                    <p style="color: #0050b3; margin-bottom: 0;">{ai_summary}</p>
                </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend server. Make sure it's running. Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
