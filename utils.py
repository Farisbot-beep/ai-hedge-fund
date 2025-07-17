import alpaca_trade_api as tradeapi
import requests
from alpaca_config import API_KEY, SECRET_KEY, BASE_URL
from datetime import datetime

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

def execute_rebalance(picks):
    current_positions = api.list_positions()
    current_symbols = [p.symbol for p in current_positions]

    # Sell positions not in the new picks
    for position in current_positions:
        if position.symbol not in picks:
            try:
                api.submit_order(
                    symbol=position.symbol,
                    qty=float(position.qty),
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                send_telegram_message(f"❌ Sold {position.symbol}")
            except Exception as e:
                send_telegram_message(f"⚠️ Sell failed for {position.symbol}: {e}")

    # Buy new picks (equal weight allocation)
    account = api.get_account()
    cash = float(account.cash)
    if not picks or cash < 10:
        send_telegram_message("⚠️ Not enough cash or no picks to rebalance.")
        return

    allocation = cash / len(picks)
    for symbol in picks:
        try:
            latest_price = float(api.get_last_trade(symbol).price)
            qty = int(allocation // latest_price)
            if qty > 0:
                api.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
                send_telegram_message(f"✅ Bought {qty} of {symbol}")
        except Exception as e:
            send_telegram_message(f"⚠️ Buy failed for {symbol}: {e}")