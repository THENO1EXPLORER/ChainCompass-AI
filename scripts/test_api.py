import json

import requests
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    params = {
        "fromChain": "POL",
        "toChain": "ARB",
        "fromToken": "USDC",
        "toToken": "ETH",
        "fromAmount": "100000000",
        "fromAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    }

    api_url = "https://li.quest/v1/quote"
    print("Sending request to LI.FI API...")
    try:
        response = requests.get(api_url, params=params, timeout=60)
        response.raise_for_status()
        quote_data = response.json()
        print("Successfully received a quote!\n")
        print(json.dumps(quote_data, indent=2))
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        if err.response is not None:
            print(f"Server Response: {err.response.text}")
    except Exception as err:  # noqa: BLE001
        print(f"Another error occurred: {err}")


if __name__ == "__main__":
    main()

