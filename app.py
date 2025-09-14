import streamlit as st
import requests

# Use the sidebar for the logo
st.sidebar.image("logo.png", use_column_width=True)

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
from_amount_display = st.number_input("Amount to Swap (e.g., 100)", value=100.0, min_value=0.0, step=1.0)

# --- The button to trigger the API call ---
if st.button("Find Best Route"):
    # Convert the user-friendly amount to the smallest unit for the API
    # Assuming 6 decimals for USDC as our primary example
    from_amount = int(from_amount_display * 10**6)

    # Define the API endpoint of your backend server
    api_url = "https://chaincompass-ai-krishnav.onrender.com/api/v1/quote"

    # The parameters for your API, taken from the input fields
    params = {
        "fromChain": from_chain,
        "toChain": to_chain,
        "fromToken": from_token,
        "toToken": to_token,
        "fromAmount": str(from_amount)
    }

    # --- Call your own API and display the result ---
    with st.spinner("Asking the AI for the best route..."):
        try:
            # Make the request to your FastAPI backend
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an error on a bad response

            result = response.json()

            st.subheader("🏆 Your AI Recommendation")

            # --- This is the updated part for the AI summary ---
            if "error" in result:
                st.error(f"An error occurred: {result.get('details', 'Unknown error')}")
            else:
                # Get the summary text from the new response format
                ai_summary = result.get("summary", "No summary available.")
                # Display the AI's sentence using markdown for better rendering
                st.markdown(f"""
                    <div style="padding: 1rem; border-radius: 0.5rem; background-color: #d4edda; border-left: 6px solid #28a745;">
                    <p style="color: #155724; margin-bottom: 0;">{ai_summary}</p>
                    </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend server. Make sure it's running. Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- About section, placed at the end to be always visible ---
with st.expander("ℹ️ About This App & How It Works"):
    st.write("""
    This app is a full-stack AI application built to simplify cross-chain swaps.
    - The **frontend** you're using is built with **Streamlit**.
    - The **backend** is a **FastAPI** server deployed on **Render**.
    - When you click the button, the frontend calls the backend, which then calls the **LI.FI API** to find the best route.
    - The complex data is then summarized by an AI using **LangChain** and presented to you.
    """)
