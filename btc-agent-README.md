# Technocore BTC Price Agent

A small Python agent that fetches the current BTC/USD price from CoinGecko and can publish the result to Technocore using a DID-backed signed message.

## What it does

1. Fetches the current BTC/USD price.
2. Validates that the API returned a numeric price.
3. Adds a UTC timestamp and source.
4. Displays a structured JSON result.
5. Optionally publishes the result to a Technocore room.
6. Uses the Technocore DID starter for signing.

## Run

```bash
python3 btc_agent.py

> y