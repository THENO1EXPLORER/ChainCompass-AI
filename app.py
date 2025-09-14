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

# --- God-Level Custom CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Create a dummy css file for demonstration, in a real scenario you would have a styles.css file
with open("styles.css", "w") as f:
    f.write("""
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* General Body Styles */
    body {
        font-family: 'Poppins', sans-serif;
    }

    /* Main App Container Background */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        background-image: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.8) 100%);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Main Title */
    h1 {
        font-weight: 600;
        letter-spacing: -1px;
    }
    
    /* Custom Card for Inputs */
    .card {
        background-color: rgba(40, 43, 54, 0.7);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }

    /* Custom Button Style */
    .stButton>button {
        color: white;
        background-image: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    /* Style for Input/Select Boxes */
    div[data-baseweb="select"] > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 0.5rem;
    }

    /* Result Display Card Animation */
    .result-card {
        padding: 1.5rem;
        border-radius: 1rem;
        background-color: rgba(24, 144, 255, 0.1);
        border-left: 6px solid #1890ff;
        color: #e6f7ff;
        animation: fadeIn 0.5s ease-in-out;
        margin-top: 1rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    """)

local_css("styles.css")

# --- Sample Data for Dropdowns ---
CHAINS = {"Polygon": "POL", "Arbitrum": "ARB", "Ethereum": "ETH", "Optimism": "OPT", "Base": "BASE"}
TOKENS = {"USDC": "USDC", "Ethereum": "ETH", "Tether": "USDT", "Wrapped BTC": "WBTC"}

# --- UI Sidebar ---
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.info("This app is a demo for the DoraHacks 'DeFiTimez Multichain Mayhem' Hackathon.")
    with st.expander("💡 How It Works", expanded=False):
        st.markdown("""
        1.  **You** enter your desired swap details.
        2.  **Our Backend** (FastAPI on Render) calls the LI.FI API to find the best swap routes.
        3.  **An AI** (GPT-4o mini via LangChain) analyzes the best route.
        4.  **You** get a simple, human-friendly summary of the optimal choice.
        """)

# --- Main Page Content ---
st.title("🧭 ChainCompass AI")
st.caption("Your smart guide for finding the best cross-chain swap routes.")

# Using markdown to create the custom card
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("⚙️ Enter Swap Details")

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

st.markdown('</div>', unsafe_allow_html=True)

if st.button("Find Best Route", type="primary", use_container_width=True):
    from_chain = CHAINS[from_chain_name]
    from_token = TOKENS[from_token_name]
    to_chain = CHAINS[to_chain_name]
    to_token = TOKENS[to_token_name]
    
    decimals = 6 if from_token == "USDC" else 18
    from_amount = int(from_amount_display * (10**decimals))
    
    api_url = "https://chaincompass-ai-krishnav.onrender.com/api/v1/quote"
    params = {
        "fromChain": from_chain, "toChain": to_chain,
        "fromToken": from_token, "toToken": to_token,
        "fromAmount": str(from_amount)
    }

    with st.spinner("Asking the AI for the best route..."):
        try:
            response = requests.get(api_url, params=params, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            st.subheader("🏆 Your AI Recommendation")

            if "error" in result:
                st.error(f"An error occurred: {result.get('details', 'Unknown error')}")
            else:
                ai_summary = result.get("summary", "No summary available.")
                st.markdown(f'<div class="result-card"><p>{ai_summary}</p></div>', unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend server. Is it running? Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

