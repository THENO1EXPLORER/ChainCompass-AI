import streamlit as st
import requests
import time
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="ChainCompass AI Suite",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Asset & Style Management ---
def apply_custom_styling():
    """Injects all custom CSS for the entire multi-page application."""
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* --- Universal Styles --- */
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #020418; /* Set a base background color */
    }
    
    /* --- Main App Background & Container --- */
    #root > div:nth-child(1) > div > div > div > div {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25' viewBox='0 0 1600 800'%3E%3Cg %3E%3Cpolygon fill='%23050928' points='1600 160 0 460 0 350 1600 50'%3E%3C/polygon%3E%3Cpolygon fill='%23080e38' points='1600 260 0 560 0 450 1600 150'%3E%3C/polygon%3E%3Cpolygon fill='%230b1348' points='1600 360 0 660 0 550 1600 250'%3E%3C/polygon%3E%3Cpolygon fill='%230e1858' points='1600 460 0 760 0 650 1600 350'%3E%3C/polygon%3E%3Cpolygon fill='%23111D68' points='1600 800 0 800 0 750 1600 450'%3E%3C/polygon%3E%3C/g%3E%3C/svg%3E");
        background-attachment: fixed;
        background-size: cover;
    }

    /* --- Sidebar Navigation --- */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 5, 30, 0.85);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1rem;
    }
    
    /* --- General UI Elements --- */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;
    }
    h1 {
        font-weight: 700;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #CF8BF3, #A770EF, #FDB99B, #CF8BF3);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShine 5s linear infinite;
    }
    @keyframes textShine { to { background-position: 200% center; } }

    /* --- Custom Card Component --- */
    .metric-card, .chart-card, .content-card {
        background: rgba(10, 5, 30, 0.75);
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease;
        height: 100%; /* Ensure cards in a row have same height */
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* --- Animations --- */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    /* Hide the default radio button circles */
    div[role="radiogroup"] > label {
        display: none;
    }
    
    """
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)


# --- Dashboard Page ---
def render_dashboard():
    st.title("📈 Analytics Dashboard")
    st.markdown("Welcome to the ChainCompass AI Suite. Here's a real-time overview of cross-chain activity.")

    # --- Metrics Row ---
    st.markdown("### Key Metrics", help="These are simulated metrics for demonstration purposes.")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="metric-card"><h4>Total Value Swapped</h4><h2>$1.2B</h2><p style="color: #4CAF50;">+2.5% last 24h</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card"><h4>Transactions (24h)</h4><h2>15,203</h2><p style="color: #F44336;">-1.8% vs yesterday</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card"><h4>Avg. Swap Time</h4><h2>85s</h2><p style="color: #4CAF50;">-12% faster</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-card"><h4>Supported Chains</h4><h2>12</h2><p>+2 new integrations</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- Charts Row ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("Swap Volume by Chain")
        df_chains = pd.DataFrame({
            'Chain': ['Polygon', 'Arbitrum', 'Optimism', 'Base', 'Ethereum'],
            'Volume': [450, 320, 210, 150, 90]
        })
        fig = go.Figure(data=[go.Bar(
            x=df_chains['Chain'], y=df_chains['Volume'],
            marker_color=['#A770EF', '#CF8BF3', '#FDB99B', '#A770EF', '#CF8BF3']
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color="white", margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("Popular Token Swaps")
        df_tokens = pd.DataFrame({
            'Token': ['USDC', 'ETH', 'USDT', 'WBTC', 'Other'],
            'Percentage': [55, 25, 12, 5, 3]
        })
        fig2 = go.Figure(data=[go.Pie(
            labels=df_tokens['Token'], values=df_tokens['Percentage'], hole=.4,
            marker_colors=['#A770EF', '#CF8BF3', '#FDB99B', '#8A2BE2', '#4B0082']
        )])
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color="white", legend_orientation="h", margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- Swap AI Page ---
def render_swap_ai():
    st.title("🤖 Swap AI Assistant")
    st.caption("Your smart guide for finding the best cross-chain swap routes.")

    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Enter Swap Details")
        CHAINS = {"Polygon": "POL", "Arbitrum": "ARB", "Ethereum": "ETH", "Optimism": "OPT", "Base": "BASE"}
        TOKENS = {"USDC": "USDC", "Ethereum": "ETH", "Tether": "USDT", "Wrapped BTC": "WBTC"}

        col1, col2 = st.columns(2)
        with col1:
            from_chain_name = st.selectbox("From Chain", options=list(CHAINS.keys()), key="from_chain")
            from_token_name = st.selectbox("Token to Swap", options=list(TOKENS.keys()), key="from_token")
        with col2:
            to_chain_name = st.selectbox("To Chain", options=list(CHAINS.keys()), index=1, key="to_chain")
            to_token_name = st.selectbox("Token to Receive", options=list(TOKENS.keys()), index=1, key="to_token")
        
        from_amount_display = st.number_input(f"Amount of {from_token_name} to Swap", value=100.0, min_value=0.01, step=10.0)
        
        if st.button("Find Best Route", type="primary", use_container_width=True):
            st.session_state.result = None
            with st.spinner("Finding the best route across the globe..."):
                api_url = "https://chaincompass-ai-krishnav.onrender.com/api/v1/quote"
                decimals = 6 if TOKENS[from_token_name] == "USDC" else 18
                params = {
                    "fromChain": CHAINS[from_chain_name], "toChain": CHAINS[to_chain_name],
                    "fromToken": TOKENS[from_token_name], "toToken": TOKENS[to_token_name],
                    "fromAmount": int(from_amount_display * (10**decimals))
                }
                try:
                    response = requests.get(api_url, params=params, timeout=60)
                    response.raise_for_status()
                    st.session_state.result = response.json()
                except Exception as e:
                    st.session_state.result = {"error": "An error occurred", "details": str(e)}
        st.markdown('</div>', unsafe_allow_html=True)

    if 'result' in st.session_state and st.session_state.result:
        if "error" in st.session_state.result:
            st.error(f"Error: {st.session_state.result.get('details', 'Unknown error')}")
        else:
            st.markdown(f'''
            <div class="content-card" style="margin-top: 2rem; border-left: 5px solid #A770EF;">
                <h3>🏆 AI Recommendation</h3>
                <p>{st.session_state.result.get("summary", "No summary available.")}</p>
            </div>
            ''', unsafe_allow_html=True)

# --- About Page ---
def render_about_page():
    st.title("📖 About ChainCompass AI")
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.image("logo.png", width=100)
    st.subheader("Mission")
    st.write("""
    ChainCompass AI solves the problem of complexity in Decentralized Finance (DeFi). Finding the best route to swap tokens across different blockchains is a confusing and risky process for most users. This application provides a simple, intuitive interface where a user can define their desired swap. The backend then queries the LI.FI aggregation API to find the optimal route based on cost and speed. Finally, the complex data is summarized into a simple, human-readable recommendation using a Large Language Model (LLM).
    """)
    st.subheader("Technology Stack")
    st.markdown("""
    - **Frontend:** Streamlit (Multi-Page App)
    - **Backend:** FastAPI, deployed on Render
    - **AI Integration:** LangChain with OpenAI (gpt-4o-mini)
    - **Data Source:** LI.FI API for live swap quotes
    - **Visualizations:** Plotly for interactive charts
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Router ---
def main():
    apply_custom_styling()

    # --- Sidebar Navigation Setup ---
    with st.sidebar:
        st.image("logo.png", use_container_width=True)
        st.header("Navigation")
        
        # This is a robust, single-file compatible navigation method
        pages = ["Dashboard", " CHAINCOMPASS-AI", "About"]
        icons = ["📊", "🤖", "📖"]
        
        if 'active_page' not in st.session_state:
            st.session_state.active_page = "Dashboard"

        # Use st.radio for state control and st.button for UI
        for page, icon in zip(pages, icons):
            if st.button(f"{icon} {page}", use_container_width=True):
                st.session_state.active_page = page
                st.rerun()

    # --- Page Rendering based on State ---
    if st.session_state.active_page == "Dashboard":
        render_dashboard()
    elif st.session_state.active_page == "Swap AI":
        render_swap_ai()
    elif st.session_state.active_page == "About":
        render_about_page()
    else:
        render_dashboard() # Default to dashboard if state is invalid

if __name__ == "__main__":
    main()

