import Logic
import requests
import json
import bscscan
import time
import web3
import dexguru
import logging
import csv
import datetime

private_key = "7c67d97cbee53f18becbef5b65905906e4f7123a6d33b98502e97c124e0def79"

def log_error(error):
    """
    Logs an error to a file.

    Args:
        error: The error to be logged.
    """

    logger = logging.getLogger(__name__)
    logger.error(error)

def main():
    # Get the list of safe tokens from the Logic.py script
    safe_tokens = Logic.get_safe_tokens()

    # Loop through the list of safe tokens
    for token_contract in safe_tokens:
        # Buy the token
        start(token_contract)

        # Monitor the price of the token
        monitor_price(token_contract, safe_tokens[token_contract]["dex"])

if __name__ == "__main__":
    main()

def start(token_contract):
    # Check to make sure that the token is safe
    if token_data is None:
        print(f"The token {token_contract} is not safe, so it will not be bought.")
        return

    # Buy the token
    web3.eth.defaultAccount = private_key
    try:
        bsc.buy(token_data["dex"], token_contract, amount, gas_price, slippage)
    except Exception as e:
        log_error(e)
        return

    # Set a sell limit order
    sell_price = token_data["price"] * 1.15  # Sell 15% above the current price
    try:
        bsc.set_sell_limit_order(token_data["dex"], token_contract, amount, sell_price, gas_price, slippage)
    except Exception as e:
        log_error(e)
        return

def monitor_price(token_contract, dex):
    # Check if the stop monitoring flag is set
    if stop_monitoring:
        return

    # Get the 5m chart data for the token
    try:
        api_key = "juDpO9t7ys4Yp5IGrTMcy-eYglvHPeenEypLvX6e4Ww"
        chart_data = dexguru.get_chart_data(token_contract, interval="5m", api_key=api_key)
    except Exception as e:
        log_error(e)
        return

    # Check if the price has dropped below a certain threshold
    current_price = chart_data["last"]
    if current_price < 0.97 * price_at_buy:
        # The price has dropped by 3%, so set a stop loss order
        sell_price = price_at_buy * 0.95  # Sell 5% below the current price
        try:
            bsc.set_sell_limit_order(dex, token_contract, amount, sell_price, gas_price, slippage)
        except Exception as e:
            log_error(e)
            return

        # Acknowledge that the stop loss order has been placed
        print("Stop loss order has been placed")

        # Check if the stop loss order has been executed
        sell_order = bsc

