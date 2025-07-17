import alpaca_trade_api as tradeapi
import requests
from alpaca_config import API_KEY, SECRET_KEY, BASE_URL

# === Alpaca Setup ===
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# === Trade Execution ===
def execute_trade(symbol, qty, side='buy'):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        print(f"✅ Trade executed: {side.upper()} {qty} of {symbol}")
    except Exception as e:
        print("❌ Trade execution failed:", e)

# === Portfolio Summary ===
def get_portfolio_summary():
    try:
        positions = api.list_positions()
        summary = []

        for pos in positions:
            symbol = pos.symbol
            qty = float(pos.qty)
            cost = float(pos.avg_entry_price)
            market_price = float(pos.current_price)
            change = ((market_price - cost) / cost) * 100

            summary.append({
                'Symbol': symbol,
                'Quantity': qty,
                'Buy Price': cost,
                'Current Price': market_price,
                'Change %': round(change, 2)
            })
        return summary
    except Exception as e:
        print("❌ Portfolio error:", e)
        return []

# === Telegram Alerts ===
def send_telegram_message(message):
    bot_token = '8084681760:AAFGXh_jm5pa6aguHdMliVr9rGkYAxLVq1I'
    chat_id = 'YOUR_CHAT_ID_HERE'  # Replace with your actual chat ID

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}

    try:
        response = requests.post(url, data=payload)
        print("📬 Telegram message sent")
    except Exception as e:
        print("❌ Telegram error:", e)