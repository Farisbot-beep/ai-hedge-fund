import yfinance as yf

def get_momentum_picks(tickers):
    picks = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if len(data) < 30:
                continue

            recent_price = data["Close"][-1]
            past_price = data["Close"][-20]

            if recent_price > past_price * 1.1:  # 10%+ increase in last month
                picks.append(ticker)
        except Exception:
            continue
    return picks