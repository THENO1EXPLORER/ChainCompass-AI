import streamlit as st
import requests
import time
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import os
from dotenv import load_dotenv

# --- Page Configuration ---
st.set_page_config(
    page_title="ChainCompass AI Suite",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables for configurable API endpoints
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "https://chaincompass-ai-krishnav.onrender.com")

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-bg: #0a0a0f;
        --card-bg: rgba(255, 255, 255, 0.05);
        --card-border: rgba(255, 255, 255, 0.1);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-accent: #00f2fe;
        --shadow-glow: 0 0 20px rgba(102, 126, 234, 0.3);
        --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    * { box-sizing: border-box; }
    
    body { 
        font-family: 'Inter', sans-serif; 
        background: var(--dark-bg);
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    
    /* Animated background */
    .main-container {
        position: relative;
        min-height: 100vh;
        background: radial-gradient(ellipse at top, #1a1a2e 0%, #16213e 50%, #0a0a0f 100%);
        overflow: hidden;
    }
    
    .main-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
        animation: backgroundShift 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes backgroundShift {
        0%, 100% { transform: translateX(0) translateY(0) scale(1); }
        33% { transform: translateX(-20px) translateY(-10px) scale(1.05); }
        66% { transform: translateX(20px) translateY(10px) scale(0.95); }
    }
    
    /* Floating particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        width: 2px;
        height: 2px;
        background: var(--text-accent);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0; }
        10%, 90% { opacity: 1; }
        50% { transform: translateY(-100px) translateX(50px); }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 15, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--card-border) !important;
        box-shadow: var(--shadow-card) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        padding: 1rem 0;
    }
    
    /* Navigation buttons */
    .nav-button {
        background: transparent !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        margin: 8px 0 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    .nav-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: var(--primary-gradient);
        transition: left 0.3s ease;
        z-index: -1;
    }
    
    .nav-button:hover {
        color: white !important;
        border-color: transparent !important;
        transform: translateX(8px) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    .nav-button:hover::before {
        left: 0;
    }
    
    .nav-button.active {
        background: var(--primary-gradient) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    /* Main content area */
    .main-content {
        padding: 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Headers */
    h1 {
        font-weight: 800 !important;
        font-size: 3rem !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin: 0 0 1rem 0 !important;
        display: flex !important;
        align-items: center !important;
        animation: titleGlow 3s ease-in-out infinite alternate !important;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.8)); }
    }
    
    h1 svg {
        width: 48px !important;
        height: 48px !important;
        margin-right: 20px !important;
        fill: url(#primaryGradient) !important;
        animation: iconPulse 2s ease-in-out infinite !important;
    }
    
    @keyframes iconPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    h2 {
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin: 2rem 0 1rem 0 !important;
        font-size: 2rem !important;
    }
    
    h3 {
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin: 1.5rem 0 0.5rem 0 !important;
        font-size: 1.5rem !important;
    }
    
    /* Cards */
    .glass-card {
        background: var(--card-bg) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: var(--shadow-card) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        animation: cardSlideIn 0.6s ease-out !important;
    }
    
    @keyframes cardSlideIn {
        from { opacity: 0; transform: translateY(30px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--primary-gradient);
        opacity: 0.6;
    }
    
    .glass-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: var(--card-bg) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-gradient);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    .metric-card h4 {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        margin: 0 0 0.5rem 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .metric-card h2 {
        color: var(--text-primary) !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 0 0 0.5rem 0 !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .metric-card p {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }
    
    /* Form elements */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stNumberInput"] > div > div {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSelectbox"] > div > div:focus-within,
    [data-testid="stNumberInput"] > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: var(--text-accent);
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Success/Error states */
    .success-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
    }
    
    .error-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Tech badges */
    .tech-badges img {
        margin: 8px !important;
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
        filter: grayscale(0.3) !important;
    }
    
    .tech-badges img:hover {
        transform: scale(1.1) translateY(-2px) !important;
        filter: grayscale(0) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-content {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h1 svg {
            width: 32px !important;
            height: 32px !important;
        }
        
        .glass-card {
            padding: 1.5rem !important;
        }
        
        .metric-card h2 {
            font-size: 2rem !important;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
    
    /* Animation delays for staggered effects */
    .glass-card:nth-child(1) { animation-delay: 0.1s; }
    .glass-card:nth-child(2) { animation-delay: 0.2s; }
    .glass-card:nth-child(3) { animation-delay: 0.3s; }
    .glass-card:nth-child(4) { animation-delay: 0.4s; }
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
    # Add floating particles effect
    st.markdown("""
    <div class="particles" id="particles"></div>
    <script>
        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
                container.appendChild(particle);
            }
        }
        createParticles();
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="48" height="48">
            <defs>
                <linearGradient id="primaryGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M3 13H5V11H3V13ZM3 17H5V15H3V17ZM3 9H5V7H3V9ZM7 13H17V11H7V13ZM7 17H17V15H7V17ZM7 9H17V7H7V9ZM19 13H21V11H19V13ZM19 17H21V15H19V17ZM19 9H21V7H19V9ZM3 21H5V19H3V21ZM7 21H17V19H7V21ZM19 21H21V19H19V21ZM3 5H5V3H3V5ZM7 5H17V3H7V5ZM19 5H21V3H19V5Z" fill="url(#primaryGradient)"></path>
        </svg>
        Analytics Dashboard
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 2rem;">
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin: 0; line-height: 1.6;">
            Welcome to the ChainCompass AI Suite. Here's a real-time overview of cross-chain activity across multiple blockchain networks.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Key Metrics")
    
    # Enhanced metrics with better styling
    m1, m2, m3, m4 = st.columns(4)
    with m1: 
        st.markdown('''
        <div class="metric-card">
            <h4>Total Value Swapped</h4>
            <h2>$1.2B</h2>
            <p style="color: #22c55e;">+2.5% last 24h</p>
        </div>
        ''', unsafe_allow_html=True)
    with m2: 
        st.markdown('''
        <div class="metric-card">
            <h4>Transactions (24h)</h4>
            <h2>15,203</h2>
            <p style="color: #ef4444;">-1.8% vs yesterday</p>
        </div>
        ''', unsafe_allow_html=True)
    with m3: 
        st.markdown('''
        <div class="metric-card">
            <h4>Avg. Swap Time</h4>
            <h2>85s</h2>
            <p style="color: #22c55e;">-12% faster</p>
        </div>
        ''', unsafe_allow_html=True)
    with m4: 
        st.markdown('''
        <div class="metric-card">
            <h4>Supported Chains</h4>
            <h2>12</h2>
            <p style="color: var(--text-accent);">+2 new integrations</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Enhanced charts section
    st.markdown("### 📈 Market Analytics")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🔗 Swap Volume by Chain")
        st.plotly_chart(generate_volume_chart(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🪙 Popular Token Swaps")
        st.plotly_chart(generate_token_pie_chart(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Add real-time activity section
    st.markdown("### ⚡ Live Activity Feed")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Simulate real-time data
    import random
    from datetime import datetime, timedelta
    
    activity_data = []
    for i in range(5):
        chains = ['Polygon', 'Arbitrum', 'Optimism', 'Base', 'Ethereum']
        tokens = ['USDC', 'ETH', 'USDT', 'WBTC']
        amounts = ['$1,250', '$5,600', '$890', '$12,400', '$3,200']
        
        activity_data.append({
            'time': (datetime.now() - timedelta(minutes=random.randint(1, 30))).strftime('%H:%M'),
            'chain': random.choice(chains),
            'token': random.choice(tokens),
            'amount': random.choice(amounts),
            'status': 'Completed'
        })
    
    for activity in activity_data:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; margin: 0.5rem 0; background: rgba(255, 255, 255, 0.03); border-radius: 8px; border-left: 3px solid var(--text-accent);">
            <div>
                <strong>{activity['amount']}</strong> {activity['token']} on <strong>{activity['chain']}</strong>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="color: var(--text-secondary); font-size: 0.9rem;">{activity['time']}</span>
                <span style="color: #22c55e; font-size: 0.8rem; background: rgba(34, 197, 94, 0.1); padding: 0.25rem 0.5rem; border-radius: 4px;">{activity['status']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_swap_ai():
    st.markdown("""
    <h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="48" height="48">
            <defs>
                <linearGradient id="aiGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M19.964 12.032c.024.314.036.63.036.952 0 4.41-3.586 8.016-8 8.016-4.41 0-8-3.605-8-8.016 0-3.352 2.06-6.234 5-7.44V2.558C4.582 3.96 1.964 7.64 1.964 12c0 5.514 4.486 10.016 10 10.016s10-4.502 10-10.016c0-.31-.013-.617-.036-.92L19.964 12.032zM12 0C9.794 0 8 1.79 8 4s1.794 4 4 4 4-1.79 4-4-1.794-4-4-4zm0 6c-1.103 0-2-.897-2-2s.897-2 2-2 2 .897 2 2-.897 2-2 2zm-4 4.016c-3.309 0-6 2.691-6 6v1.984h12v-1.984c0-3.309-2.691-6-6-6zm0 2c2.206 0 4 1.794 4 4v.016H4v-.016c0-2.206 1.794-4 4-4z" fill="url(#aiGradient)"></path>
        </svg>
        Swap AI Assistant
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 2rem;">
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin: 0; line-height: 1.6;">
            Your intelligent guide for finding the optimal cross-chain swap routes. Our AI analyzes multiple DEXs and bridges to find the best rates, lowest fees, and fastest execution times.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced swap form
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🔄 Configure Your Swap")
    
    CHAINS = {
        "Polygon": {"code": "POL", "icon": "🟣", "color": "#8247e5"},
        "Arbitrum": {"code": "ARB", "icon": "🔵", "color": "#28a0f0"},
        "Ethereum": {"code": "ETH", "icon": "⚫", "color": "#627eea"},
        "Optimism": {"code": "OPT", "icon": "🔴", "color": "#ff0420"},
        "Base": {"code": "BASE", "icon": "🔷", "color": "#0052ff"}
    }
    
    TOKENS = {
        "USDC": {"code": "USDC", "icon": "💵", "decimals": 6},
        "Ethereum": {"code": "ETH", "icon": "Ξ", "decimals": 18},
        "Tether": {"code": "USDT", "icon": "💸", "decimals": 6},
        "Wrapped BTC": {"code": "WBTC", "icon": "₿", "decimals": 8}
    }
    
    # Chain selection with visual indicators
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**From Chain**")
        from_chain_name = st.selectbox("", options=list(CHAINS.keys()), key="from_chain", label_visibility="collapsed")
        if from_chain_name:
            chain_info = CHAINS[from_chain_name]
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin-top: 0.5rem;">
                <span style="font-size: 1.5rem;">{chain_info['icon']}</span>
                <span style="color: {chain_info['color']}; font-weight: 600;">{from_chain_name}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**Token to Swap**")
        from_token_name = st.selectbox("", options=list(TOKENS.keys()), key="from_token", label_visibility="collapsed")
        if from_token_name:
            token_info = TOKENS[from_token_name]
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin-top: 0.5rem;">
                <span style="font-size: 1.2rem;">{token_info['icon']}</span>
                <span style="font-weight: 600;">{from_token_name}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**To Chain**")
        to_chain_name = st.selectbox("", options=list(CHAINS.keys()), index=1, key="to_chain", label_visibility="collapsed")
        if to_chain_name:
            chain_info = CHAINS[to_chain_name]
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin-top: 0.5rem;">
                <span style="font-size: 1.5rem;">{chain_info['icon']}</span>
                <span style="color: {chain_info['color']}; font-weight: 600;">{to_chain_name}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**Token to Receive**")
        to_token_name = st.selectbox("", options=list(TOKENS.keys()), index=1, key="to_token", label_visibility="collapsed")
        if to_token_name:
            token_info = TOKENS[to_token_name]
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin-top: 0.5rem;">
                <span style="font-size: 1.2rem;">{token_info['icon']}</span>
                <span style="font-weight: 600;">{to_token_name}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick amount buttons
    st.markdown("**Quick Amounts**")
    quick_cols = st.columns(5)
    quick_amounts = [50.0, 100.0, 500.0, 1000.0, 5000.0]
    for i, amount in enumerate(quick_amounts):
        with quick_cols[i]:
            if st.button(f"${amount}", key=f"quick_{amount}", use_container_width=True):
                st.session_state["desired_amount"] = float(amount)
                st.rerun()

    # Amount input with enhanced styling (widget key distinct from session key)
    st.markdown("**Amount to Swap**")
    from_amount_display = st.number_input(
        f"Enter amount of {from_token_name} to swap", 
        value=float(st.session_state.get("desired_amount", 100.0)), 
        min_value=0.01, 
        step=10.0,
        key="amount_input_widget",
        label_visibility="collapsed"
    )
    
    # Enhanced swap button with loading state
    if st.button("🚀 Find Best Route", type="primary", use_container_width=True):
        st.session_state.result = None
        st.session_state.loading = True
        
        # Show loading animation
        with st.spinner("🔍 Analyzing routes across multiple DEXs and bridges..."):
            api_url = f"{API_BASE_URL.rstrip('/')}/api/v1/quote"
            decimals = TOKENS[from_token_name]["decimals"]
            params = { 
                "fromChain": CHAINS[from_chain_name]["code"], 
                "toChain": CHAINS[to_chain_name]["code"], 
                "fromToken": TOKENS[from_token_name]["code"], 
                "toToken": TOKENS[to_token_name]["code"], 
                "fromAmount": str(int(from_amount_display * (10**decimals))) 
            }
            
            try:
                response = requests.get(api_url, params=params, timeout=60)
                response.raise_for_status()
                st.session_state.result = response.json()
                st.session_state.loading = False
            except requests.exceptions.HTTPError as http_err:
                try:
                    err_json = response.json()
                except Exception:
                    err_json = {"details": response.text}
                st.session_state.result = {"error": "Failed to fetch quote", **err_json, "status_code": response.status_code}
                st.session_state.loading = False
            except requests.exceptions.Timeout:
                st.session_state.result = {"error": "Request timed out", "details": "The request took too long. Please try again."}
                st.session_state.loading = False
            except Exception as e:
                st.session_state.result = {"error": "An unexpected error occurred", "details": str(e)}
                st.session_state.loading = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced results display
    if 'result' in st.session_state and st.session_state.result:
        result = st.session_state.result
        if result.get("error"):
            st.markdown('<div class="glass-card error-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Error")
            st.markdown(f"**{result.get('error')}**")
            if result.get("details"):
                with st.expander("🔍 Technical Details"):
                    st.code(str(result.get("details")))
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card success-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
            st.markdown("#### 🏆 AI Recommendation")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.3);">
                <p style="font-size: 1.1rem; line-height: 1.6; margin: 0; color: var(--text-primary);">
                    {result.get("summary", "")}
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def render_about_page():
    st.markdown("""
    <h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="48" height="48">
            <defs>
                <linearGradient id="aboutGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8zm-1-5h2v2h-2v-2zm0-8h2v6h-2V7z" fill="url(#aboutGradient)"></path>
        </svg>
        About ChainCompass AI
    </h1>
    """, unsafe_allow_html=True)
    
    # Mission section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Our Mission")
    st.markdown("""
    <p style="font-size: 1.1rem; line-height: 1.6; color: var(--text-secondary);">
        ChainCompass AI revolutionizes cross-chain DeFi by making complex token swaps simple, secure, and intelligent. 
        We bridge the gap between multiple blockchain networks, providing users with the best routes, lowest fees, 
        and fastest execution times through advanced AI analysis.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Developer section
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(get_logo_as_html(width="120px"), unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center; color: var(--text-primary);'>Krishnav Mahajan</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: var(--text-accent); font-weight: 600;'>Lead Developer & AI Engineer</p>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <p style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5;">
                Full-stack developer specializing in DeFi protocols, AI integration, and blockchain technology. 
                Passionate about creating user-friendly solutions for complex financial systems.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🛠️ Technology Stack")
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
        
        st.markdown("#### 🚀 Key Features")
        features = [
            "🤖 AI-Powered Route Optimization",
            "🔗 Multi-Chain Support (12+ Networks)",
            "⚡ Real-Time Market Analysis", 
            "💰 Lowest Fee Discovery",
            "🛡️ Secure & Trustless Swaps",
            "📊 Advanced Analytics Dashboard"
        ]
        
        for feature in features:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                <span style="font-size: 1.2rem; margin-right: 0.75rem;">{feature.split(' ')[0]}</span>
                <span style="color: var(--text-primary);">{' '.join(feature.split(' ')[1:])}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats section
    st.markdown("#### 📈 Project Statistics")
    stats_cols = st.columns(4)
    stats = [
        {"label": "Supported Chains", "value": "12+", "icon": "🔗"},
        {"label": "DEXs Integrated", "value": "50+", "icon": "🏪"},
        {"label": "AI Models", "value": "3", "icon": "🧠"},
        {"label": "Uptime", "value": "99.9%", "icon": "⚡"}
    ]
    
    for i, stat in enumerate(stats):
        with stats_cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{stat['icon']}</div>
                <h2>{stat['value']}</h2>
                <h4>{stat['label']}</h4>
            </div>
            """, unsafe_allow_html=True)

# --- Main App Router ---
def main():
    apply_custom_styling()
    
    with st.sidebar:
        st.markdown(get_logo_as_html(), unsafe_allow_html=True)
        st.markdown("### Navigation")
        
        pages = {
            "Dashboard": {"icon": "📊", "desc": "Analytics & Overview"},
            "Swap AI": {"icon": "🤖", "desc": "AI-Powered Swaps"},
            "About": {"icon": "ℹ️", "desc": "Project Information"}
        }
        
        if 'active_page' not in st.session_state:
            st.session_state.active_page = "Dashboard"

        # Enhanced navigation with descriptions
        for page, info in pages.items():
            is_active = (page == st.session_state.active_page)
            
            if st.button(f"{info['icon']} {page}", key=f"nav_{page}", use_container_width=True):
                st.session_state.active_page = page
                st.rerun()
            
            if is_active:
                st.markdown(f"""
                <div style="padding: 0.5rem; margin: 0.25rem 0; background: rgba(102, 126, 234, 0.1); border-radius: 8px; border-left: 3px solid var(--text-accent);">
                    <p style="margin: 0; font-size: 0.85rem; color: var(--text-secondary);">{info['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick stats in sidebar
        st.markdown("### Quick Stats")
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 12px; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: var(--text-secondary);">Active Swaps:</span>
                <span style="color: var(--text-accent); font-weight: 600;">1,247</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: var(--text-secondary);">Total Volume:</span>
                <span style="color: var(--text-accent); font-weight: 600;">$2.1M</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: var(--text-secondary);">Avg. Fee:</span>
                <span style="color: var(--text-accent); font-weight: 600;">0.12%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # JavaScript for enhanced interactions
        components.html(f"""
            <script>
                // Add hover effects to navigation buttons
                var navButtons = parent.document.querySelectorAll('[data-testid="stSidebar"] button');
                navButtons.forEach(function(button) {{
                    button.addEventListener('mouseenter', function() {{
                        this.style.transform = 'translateX(8px)';
                        this.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.3)';
                    }});
                    button.addEventListener('mouseleave', function() {{
                        this.style.transform = 'translateX(0)';
                        this.style.boxShadow = 'none';
                    }});
                }});
            </script>
        """, height=0)

    # Render the active page
    page_functions = {"Dashboard": render_dashboard, "Swap AI": render_swap_ai, "About": render_about_page}
    page_functions[st.session_state.active_page]()

if __name__ == "__main__":
    main()

