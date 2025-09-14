import streamlit as st
import requests
import time
import streamlit.components.v1 as components
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="ChainCompass AI",
    page_icon="🧭",
    layout="wide",  # Use wide layout for the 3D globe
    initial_sidebar_state="auto"
)

# --- Asset & Style Management ---
def local_css(file_name):
    with open(file_name, "w") as f:
        f.write("""
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        /* --- General Body & Font --- */
        body { font-family: 'Poppins', sans-serif; overflow: hidden; }

        /* --- 3D Globe Background Container --- */
        #globe-container {
            position: fixed;
            width: 100vw;
            height: 100vh;
            top: 0;
            left: 0;
            z-index: -2;
        }

        /* --- Aurora Mouse Effect --- */
        #cursor-aurora {
            position: fixed;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(167, 112, 239, 0.3) 0%, rgba(167, 112, 239, 0) 60%);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%);
            transition: all 0.2s ease-out;
            z-index: -1;
        }

        /* --- Main App Container --- */
        .main .block-container {
            max-width: 700px;
            margin: 0 auto;
            padding-top: 5rem;
            z-index: 1;
        }
        
        /* --- Holographic Card UI --- */
        .card {
            background: rgba(10, 5, 30, 0.75);
            border-radius: 1.5rem;
            padding: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.15);
            margin-bottom: 2rem;
            backdrop-filter: blur(20px);
            transform-style: preserve-3d;
            transform: perspective(1000px);
            transition: transform 0.1s ease;
        }

        /* --- Animated Gradient Title --- */
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
        
        /* --- Result Card --- */
        .result-card {
            border-left: 5px solid #A770EF;
            animation: slideInUp 0.6s ease-out;
        }
        @keyframes slideInUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

        /* --- Animated Route Visualization --- */
        .route-viz { display: flex; align-items: center; justify-content: space-between; padding: 1rem 0; color: white; }
        .route-viz .chain { text-align: center; font-weight: 600; }
        .route-viz .line {
            flex-grow: 1; height: 2px;
            background: linear-gradient(90deg, #A770EF, #CF8BF3);
            transform: scaleX(0); transform-origin: left;
            animation: drawLine 0.5s ease-out forwards;
            animation-delay: 0.3s;
            margin: 0 1rem;
        }
        @keyframes drawLine { to { transform: scaleX(1); } }
        """)
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def local_js(file_name):
    with open(file_name, "w") as f:
        f.write("""
        const aurora = document.getElementById('cursor-aurora');
        const card = document.querySelector('.card');

        document.addEventListener('mousemove', (e) => {
            if (aurora) {
                aurora.style.left = e.clientX + 'px';
                aurora.style.top = e.clientY + 'px';
            }
            if(card) {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const rotateX = (y - rect.height / 2) / 20;
                const rotateY = -(x - rect.width / 2) / 20;
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
            }
        });

        if(card) {
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            });
        }
        """)
    with open(file_name) as f:
        components.html(f'<script>{f.read()}</script>', height=0)

# --- Inject Assets into Streamlit ---
local_css("styles.css")
components.html('<div id="globe-container"></div><div id="cursor-aurora"></div>', height=0)

# Inject 3D Globe library and initialization script
components.html("""
    <script src="//unpkg.com/three"></script>
    <script src="//unpkg.com/three-globe"></script>
    <script>
        const globe = Globe()
            .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
            .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
            .backgroundColor('rgba(0,0,0,0)')
            .arcsData([...Array(20).keys()].map(() => ({
                startLat: (Math.random() - 0.5) * 180,
                startLng: (Math.random() - 0.5) * 360,
                endLat: (Math.random() - 0.5) * 180,
                endLng: (Math.random() - 0.5) * 360,
                color: [['#CF8BF3', '#A770EF', '#FDB99B'][Math.round(Math.random() * 2)], ['#CF8BF3', '#A770EF', '#FDB99B'][Math.round(Math.random() * 2)]]
            })))
            .arcColor('color')
            .arcDashLength(() => Math.random())
            .arcDashGap(() => Math.random())
            .arcDashAnimateTime(() => Math.random() * 4000 + 500)
            .arcStroke(0.3)
            (document.getElementById('globe-container'));

        globe.controls().autoRotate = true;
        globe.controls().autoRotateSpeed = 0.2;
        globe.controls().enableZoom = false;
    </script>
""", height=0, scrolling=False)

# --- App State Management ---
if 'result' not in st.session_state:
    st.session_state.result = None

# --- UI Sidebar ---
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.info("Demo for the DoraHacks 'DeFiTimez Multichain Mayhem' Hackathon.")
    with st.expander("💡 How It Works", expanded=True):
        st.markdown("""
        1.  **Enter Swap Details** in the interactive holographic card.
        2.  **Backend on Render** calls the LI.FI API for the optimal route.
        3.  **An AI (GPT-4o mini)** analyzes the complex data.
        4.  **Receive a Visual Summary** below, complete with an animated diagram.
        """)

# --- Main Page Content ---
st.title("🧭 ChainCompass AI")
st.caption("Your smart guide for finding the best cross-chain swap routes.")

# Input Card
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# Button logic and API call
if st.button("Find Best Route", type="primary", use_container_width=True):
    st.session_state.result = None # Clear previous results
    
    with st.spinner("Finding the best route across the globe..."):
        time.sleep(2) # Simulate work
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

# Display Result
if st.session_state.result:
    if "error" in st.session_state.result:
        st.error(f"Error: {st.session_state.result.get('details', 'Unknown error')}")
    else:
        st.markdown(f'''
        <div class="result-card card">
            <h3>🏆 AI Recommendation</h3>
            <p>{st.session_state.result.get("summary", "No summary available.")}</p>
            <div class="route-viz">
                 <div class="chain"><span>{from_chain_name}</span></div>
                 <div class="line"></div>
                 <div class="chain"><span>Protocol</span></div>
                 <div class="line"></div>
                 <div class="chain"><span>{to_chain_name}</span></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# Inject the final JS for mouse effects
local_js("effects.js")

