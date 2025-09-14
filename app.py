import streamlit as st
import requests
import pandas as pd
import base64
import streamlit.components.v1 as components # <-- ADDED THIS IMPORT

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

# This is a more advanced technique to inject JavaScript for the mouse-following glow effect
def inject_js():
    js = """
    <script>
        const card = document.querySelector('.card');
        if (card) {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        }
    </script>
    """
    # Use the new components import here
    components.html(js, height=0)

# Create the CSS file with all the new styles
with open("styles.css", "w") as f:
    f.write("""
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* --- General Body & Font Styles --- */
    body {
        font-family: 'Poppins', sans-serif;
    }

    /* --- Animated Gradient Background --- */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- Sidebar Styling --- */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 12, 41, 0.8);
        backdrop-filter: blur(5px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }

    /* --- Main Content Headers --- */
    h1, h3 {
        color: #FFFFFF;
        font-weight: 700;
        letter-spacing: -1px;
    }
    .st-emotion-cache-10trblm { /* Caption style */
        color: rgba(255, 255, 255, 0.6);
    }

    /* --- Interactive Glow Card --- */
    .card {
        background: rgba(36, 36, 62, 0.6);
        border-radius: 1rem;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(97, 97, 255, 0.4) 0%, rgba(97, 97, 255, 0) 70%);
        left: var(--mouse-x, -100px);
        top: var(--mouse-y, -100px);
        transform: translate(-50%, -50%);
        transition: left 0.2s ease, top 0.2s ease;
        pointer-events: none; /* Allows clicks to pass through */
    }

    /* --- Styled Button --- */
    .stButton>button {
        color: white;
        font-weight: 600;
        padding: 0.8rem 1.6rem;
        border-radius: 0.5rem;
        background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    .stButton>button:active {
        transform: translateY(0px); /* Click down effect */
    }

    /* --- Styled Inputs --- */
    div[data-baseweb="select"] > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }

    /* --- Final Result Card --- */
    .result-card {
        background: rgba(36, 36, 62, 0.8);
        border-left: 5px solid #667eea;
        border-radius: 1rem;
        padding: 1.5rem;
        animation: fadeIn 0.5s ease-in-out;
        margin-top: 1.5rem;
    }
    .result-card h3 {
        margin-top: 0;
        margin-bottom: 0.5rem;
        color: #FFFFFF;
    }
    .result-card p {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.98); }
        to { opacity: 1; transform: scale(1); }
    }

    /* --- Custom Scrollbar --- */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f0c29; }
    ::-webkit-scrollbar-thumb { background: #667eea; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #764ba2; }
    """)

local_css("styles.css")

# --- Sample Data for Dropdowns ---
CHAINS = {"Polygon": "POL", "Arbitrum": "ARB", "Ethereum": "ETH", "Optimism": "OPT", "Base": "BASE"}
TOKENS = {"USDC": "USDC", "Ethereum": "ETH", "Tether": "USDT", "Wrapped BTC": "WBTC"}

# --- UI Sidebar ---
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.info("This app is a demo for the DoraHacks 'DeFiTimez Multichain Mayhem' Hackathon.")
    with st.expander("💡 How It Works", expanded=True):
        st.markdown("""
        1.  **Enter Swap Details** in the interactive card.
        2.  **Backend on Render** calls the LI.FI API to find the optimal route.
        3.  **An AI (GPT-4o mini)** analyzes the complex data.
        4.  **Receive a Simple Summary** in the animated result card below.
        """)

# --- Main Page Content ---
st.title("🧭 ChainCompass AI")
st.caption("Your smart guide for finding the best cross-chain swap routes.")

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
    value=100.0, min_value=0.01, step=10.0,
    help="Enter the amount of the token you want to swap."
)
st.markdown('</div>', unsafe_allow_html=True)
# This injects the JS needed for the glow effect AFTER the card element is created
inject_js()

if st.button("Find Best Route", type="primary", use_container_width=True):
    from_chain = CHAINS[from_chain_name]
    from_token = TOKENS[from_token_name]
    to_chain = CHAINS[to_chain_name]
    to_token = TOKENS[to_token_name]
    
    decimals = 6 if from_token == "USDC" else 18
    from_amount = int(from_amount_display * (10**decimals))
    
    api_url = "https://chaincompass-ai-krishnav.onrender.com/api/v1/quote"
    params = {"fromChain": from_chain, "toChain": to_chain, "fromToken": from_token, "toToken": to_token, "fromAmount": str(from_amount)}

    with st.spinner("Asking the AI for the best route..."):
        try:
            response = requests.get(api_url, params=params, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                st.error(f"An error occurred: {result.get('details', 'Unknown error')}")
            else:
                ai_summary = result.get("summary", "No summary available.")
                st.markdown(f'''
                <div class="result-card">
                    <h3>🏆 AI Recommendation</h3>
                    <p>{ai_summary}</p>
                </div>
                ''', unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend server. Is it running? Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

