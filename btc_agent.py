import json
import subprocess
import urllib.request
from datetime import datetime, timezone


API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
TECHNOCORE_DIR = "/Users/paiin/technocore-did-starter"


def fetch_btc_price():
    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "Technocore-BTC-Agent/1.0"},
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode())

    price = data["bitcoin"]["usd"]

    if not isinstance(price, (int, float)):
        raise ValueError("API returned an invalid BTC price")

    return {
        "task": "btc_price",
        "asset": "BTC",
        "currency": "USD",
        "price": price,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "CoinGecko",
        "status": "success",
    }


def publish_to_technocore(result):
    message = (
        f"BTC/USD is ${result['price']:,.2f}. "
        f"Source: {result['source']}. "
        f"Fetched: {result['timestamp']}."
    )

    command = [
        "python",
        "technocore_agent.py",
        "say",
        "technocore",
        message,
    ]

    subprocess.run(
        command,
        cwd=TECHNOCORE_DIR,
        check=True,
    )


def main():
    try:
        result = fetch_btc_price()

        print("\nBTC Price Agent")
        print("================")
        print(f"BTC/USD: ${result['price']:,.2f}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Source: {result['source']}")
        print(f"Status: {result['status']}")

        print("\nJSON:")
        print(json.dumps(result, indent=2))

        answer = input("\nPublish this result to Technocore? [y/N]: ")

        if answer.lower() == "y":
            print("\nPublishing to Technocore...")
            publish_to_technocore(result)
            print("Published successfully.")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()