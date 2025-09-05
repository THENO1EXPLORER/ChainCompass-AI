from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

# --- 1. Define the AI Model and Prompt Template ---

# Initialize the OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini")

# Create a template that tells the AI what to do
# It takes our clean summary data as input
prompt = ChatPromptTemplate.from_template(
    "You are a helpful crypto assistant called ChainCompass. "
    "Summarize the following best route for a user in a friendly, single sentence. "
    "Mention the provider, the estimated time, the final amount in USD, and the fees. "
    "Route details: Provider={provider}, Time={time_seconds}s, Fees=${fees_usd:.2f}, Output=${output_usd:.2f}"
)

# --- 2. Create the AI Chain ---
# A chain combines the prompt and the model
chain = prompt | llm

# --- 3. Test with Sample Data ---

# This is the clean summary data our parser function creates
sample_summary = {
    "provider": "AcrossV4",
    "time_seconds": 48,
    "fees_usd": 0.28,
    "output_usd": 99.06
}

print("🤖 Generating AI summary...")
# Invoke the chain with our sample data
response = chain.invoke(sample_summary)

# The 'content' attribute holds the AI's text response
ai_summary = response.content
print(ai_summary)
