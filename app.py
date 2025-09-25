import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="ChainCompass AI Suite",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Asset & Style Management ---
@st.cache_data
def get_logo_as_html(width="100%"):
    """Returns the SVG code for the logo as an HTML string."""
    logo_svg = f"""
    <svg width="{width}" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#A770EF;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#CF8BF3;stop-opacity:1" />
            </linearGradient>
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="5" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        <circle cx="75" cy="75" r="65" fill="rgba(10, 5, 30, 0.75)" stroke="url(#grad1)" stroke-width="2" filter="url(#glow)"/>
        <path d="M75 20 L85 65 L75 55 L65 65 Z" fill="url(#grad1)"/>
        <path d="M75 130 L65 85 L75 95 L85 85 Z" fill="url(#grad1)" opacity="0.7"/>
        <path d="M20 75 L65 85 L55 75 L65 65 Z" fill="url(#grad1)" opacity="0.7"/>
        <path d="M130 75 L85 65 L95 75 L85 85 Z" fill="url(#grad1)" opacity="0.7"/>
        <circle cx="75" cy="75" r="15" fill="#020418"/>
        <text x="75" y="82" font-family="Poppins, sans-serif" font-size="14" fill="#CF8BF3" text-anchor="middle" font-weight="600">AI</text>
    </svg>
    """
    style = "padding: 1rem;"
    if width != "100%":
        style += f" width: {width};"
    return f'<div style="{style}">{logo_svg}</div>'

def apply_custom_styling():
    """Injects all custom CSS for the entire multi-page application."""
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    body { font-family: 'Poppins', sans-serif; background-color: #020418; }
    #root > div:nth-child(1) > div > div > div > div {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25' viewBox='0 0 1600 800'%3E%3Cg %3E%3Cpolygon fill='%23050928' points='1600 160 0 460 0 350 1600 50'%3E%3C/polygon%3E%3Cpolygon fill='%23080e38' points='1600 260 0 560 0 450 1600 150'%3E%3C/polygon%3E%3Cpolygon fill='%230b1348' points='1600 360 0 660 0 550 1600 250'%3E%3C/polygon%3E%3Cpolygon fill='%230e1858' points='1600 460 0 760 0 650 1600 350'%3E%3C/polygon%3E%3Cpolygon fill='%23111D68' points='1600 800 0 800 0 750 1600 450'%3E%3C/polygon%3E%3C/g%3E%3C/svg%3E");
        background-attachment: fixed; background-size: cover;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 5, 30, 0.85); backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stButton > button {
        background-color: transparent; color: #FFFFFF; border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.2s ease-in-out; font-weight: 600; margin-bottom: 0.5rem; text-align: left; padding: 0.75rem !important;
    }
    .stButton > button:hover {
        background-color: rgba(167, 112, 239, 0.2); color: #CF8BF3; border-color: #A770EF;
    }
    .stButton > button.active_button {
        background-color: #A770EF; color: white; border-color: #A770EF;
    }
    h1 {
        font-weight: 700; background: linear-gradient(90deg, #CF8BF3, #A770EF, #FDB99B, #CF8BF3);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: textShine 5s linear infinite, fadeIn 0.8s ease; display: flex; align-items: center;
    }
    h1 svg { width: 40px; height: 40px; margin-right: 15px; fill: #CF8BF3; }
    h3 { margin-top: 2rem; margin-bottom: 1rem; } /* Style for chart titles */
    @keyframes textShine { to { background-position: 200% center; } }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div, 
    [data-testid="stNumberInput"] div[data-baseweb="input"] > div {
        background-color: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #A770EF, #CF8BF3); color: white; border: none;
    }
    .stButton > button[kind="primary"]:hover { box-shadow: 0 0 15px #A770EF; transform: translateY(-2px); }
    .metric-card, .chart-card, .content-card {
        background: rgba(10, 5, 30, 0.75); border-radius: 1rem; padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15); backdrop-filter: blur(20px);
        height: 100%; animation: fadeIn 0.8s ease;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    .tech-badges img { margin: 5px; transition: transform 0.2s ease; }
    .tech-badges img:hover { transform: scale(1.1); }
    """
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# --- Caching Data Generation Functions ---
@st.cache_data
def generate_volume_chart():
    df_chains = pd.DataFrame({'Chain': ['Polygon', 'Arbitrum', 'Optimism', 'Base', 'Ethereum'],'Volume (Millions)': [450, 320, 210, 150, 90]})
    fig = go.Figure(data=[go.Bar(x=df_chains['Chain'], y=df_chains['Volume (Millions)'], marker_color=['#A770EF', '#CF8BF3', '#FDB99B', '#A770EF', '#CF8BF3'])])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=20, r=20, t=20, b=20))
    return fig

@st.cache_data
def generate_token_pie_chart():
    df_tokens = pd.DataFrame({'Token': ['USDC', 'ETH', 'USDT', 'WBTC', 'Other'], 'Percentage': [55, 25, 12, 5, 3]})
    fig = go.Figure(data=[go.Pie(labels=df_tokens['Token'], values=df_tokens['Percentage'], hole=.4, marker_colors=['#A770EF', '#CF8BF3', '#FDB99B', '#8A2BE2', '#4B0082'])])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", legend_orientation="h", margin=dict(l=20, r=20, t=20, b=20))
    return fig

# --- Page Rendering Functions ---
def render_dashboard():
    # ... (SVG icon and title are the same)
    st.markdown("""
    <h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="40" height="40"><path d="M3 13H5V11H3V13ZM3 17H5V15H3V17ZM3 9H5V7H3V9ZM7 13H17V11H7V13ZM7 17H17V15H7V17ZM7 9H17V7H7V9ZM19 13H21V11H19V13ZM19 17H21V15H19V17ZM19 9H21V7H19V9ZM3 21H5V19H3V21ZM7 21H17V19H7V21ZM19 21H21V19H19V21ZM3 5H5V3H3V5ZM7 5H17V3H7V5ZM19 5H21V3H19V5Z"></path></svg>
        Analytics Dashboard
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("Welcome to the ChainCompass AI Suite. Here's a real-time overview of cross-chain activity.")
    st.markdown("### Key Metrics", help="These are simulated metrics for demonstration purposes.")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown('<div class="metric-card"><h4>Total Value Swapped</h4><h2>$1.2B</h2><p style="color: #4CAF50;">+2.5% last 24h</p></div>', unsafe_allow_html=True)
    with m2: st.markdown('<div class="metric-card"><h4>Transactions (24h)</h4><h2>15,203</h2><p style="color: #F44336;">-1.8% vs yesterday</p></div>', unsafe_allow_html=True)
    with m3: st.markdown('<div class="metric-card"><h4>Avg. Swap Time</h4><h2>85s</h2><p style="color: #4CAF50;">-12% faster</p></div>', unsafe_allow_html=True)
    with m4: st.markdown('<div class="metric-card"><h4>Supported Chains</h4><h2>12</h2><p>+2 new integrations</p></div>', unsafe_allow_html=True)
    
    # --- FIXED LAYOUT ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Swap Volume by Chain")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(generate_volume_chart(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.subheader("Popular Token Swaps")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(generate_token_pie_chart(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_swap_ai():
    # ... (SVG icon and title are the same)
    st.markdown("""
    <h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="40" height="40"><path d="M19.964 12.032c.024.314.036.63.036.952 0 4.41-3.586 8.016-8 8.016-4.41 0-8-3.605-8-8.016 0-3.352 2.06-6.234 5-7.44V2.558C4.582 3.96 1.964 7.64 1.964 12c0 5.514 4.486 10.016 10 10.016s10-4.502 10-10.016c0-.31-.013-.617-.036-.92L19.964 12.032zM12 0C9.794 0 8 1.79 8 4s1.794 4 4 4 4-1.79 4-4-1.794-4-4-4zm0 6c-1.103 0-2-.897-2-2s.897-2 2-2 2 .897 2 2-.897 2-2 2zm-4 4.016c-3.309 0-6 2.691-6 6v1.984h12v-1.984c0-3.309-2.691-6-6-6zm0 2c2.206 0 4 1.794 4 4v.016H4v-.016c0-2.206 1.794-4 4-4z"></path></svg>
        Swap AI Assistant
    </h1>
    """, unsafe_allow_html=True)
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
            with st.spinner("Finding the best route..."):
                api_url = "https://chaincompass-ai-krishnav.onrender.com/api/v1/quote"
                decimals = 6 if TOKENS[from_token_name] == "USDC" else 18
                params = { "fromChain": CHAINS[from_chain_name], "toChain": CHAINS[to_chain_name], "fromToken": TOKENS[from_token_name], "toToken": TOKENS[to_token_name], "fromAmount": str(int(from_amount_display * (10**decimals))) }
                try:
                    response = requests.get(api_url, params=params, timeout=60)
                    response.raise_for_status()
                    st.session_state.result = response.json()
                except Exception as e:
                    st.session_state.result = {"error": "An unexpected error occurred", "details": str(e)}
        st.markdown('</div>', unsafe_allow_html=True)
    if 'result' in st.session_state and st.session_state.result:
        st.markdown(f'''<div class="content-card" style="margin-top: 2rem;"><h3>🏆 AI Recommendation</h3><p>{st.session_state.result.get("summary", "")}</p></div>''', unsafe_allow_html=True)

def render_about_page():
    # ... (SVG icon and title are the same)
    st.markdown("""
    <h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="40" height="40"><path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8zm-1-5h2v2h-2v-2zm0-8h2v6h-2V7z"></path></svg>
        About ChainCompass AI
    </h1>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(get_logo_as_html(width="120px"), unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center;'>Krishnav Mahajan</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #CF8BF3;'>Lead Developer</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Mission")
        st.write("ChainCompass AI solves the problem of complexity in Decentralized Finance (DeFi)...")
        st.subheader("Technology Stack")
        st.markdown("""
            <div class="tech-badges">
                <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
                <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
                <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
                <img src="https://img.shields.io/badge/LangChain-182333?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
                <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
                <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render">
                <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Router ---
def main():
    apply_custom_styling()
    
    with st.sidebar:
        st.markdown(get_logo_as_html(), unsafe_allow_html=True)
        st.header("Navigation")
        pages = {"Dashboard": "📈", "Swap AI": "🤖", "About": "📖"}
        
        if 'active_page' not in st.session_state:
            st.session_state.active_page = "Dashboard"

        # This is the corrected, robust navigation logic
        active_page_name = st.session_state.active_page
        for page, icon in pages.items():
            
            # Using st.markdown to create a custom button with a class (omitted)
            
            if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True):
                 st.session_state.active_page = page
                 st.rerun()

        # JavaScript hack to apply the active class
        components.html(f"""
            <script>
                var buttons = parent.document.querySelectorAll('[data-testid="stSidebar"] button');
                var activePage = "{active_page_name}";
                buttons.forEach(function(button) {{
                    if (button.innerText.includes(activePage)) {{
                        button.classList.add('active_button');
                    }} else {{
                        button.classList.remove('active_button');
                    }}
                }});
            </script>
        """, height=0)

    # Render the active page
    page_functions = {"Dashboard": render_dashboard, "Swap AI": render_swap_ai, "About": render_about_page}
    page_functions[st.session_state.active_page]()

if __name__ == "__main__":
    main()

