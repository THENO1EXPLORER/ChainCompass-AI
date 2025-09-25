from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful crypto assistant called ChainCompass. "
        "Summarize the following best route for a user in a friendly, single sentence. "
        "Mention the provider, the estimated time, the final amount in USD, and the fees. "
        "Route details: Provider={provider}, Time={time_seconds}s, Fees=${fees_usd:.2f}, Output=${output_usd:.2f}"
    )

    chain = prompt | llm

    sample_summary = {
        "provider": "AcrossV4",
        "time_seconds": 48,
        "fees_usd": 0.28,
        "output_usd": 99.06,
    }

    print("Generating AI summary...")
    response = chain.invoke(sample_summary)
    print(response.content)


if __name__ == "__main__":
    main()

