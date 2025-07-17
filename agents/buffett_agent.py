import yfinance as yf

# Optional: Define some known Buffett-style stocks as fallback
known_buffett_holdings = [
    "AAPL", "KO", "AXP", "MCO", "BAC", "CVX", "OXY", "KHC", "V", "MA", "USB", "CE", "HPQ"
]

def get_buffett_recommendations(tickers):
    picks = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            pe = info.get("trailingPE")
            roe = info.get("returnOnEquity")
            debt_equity = info.get("debtToEquity")

            # Basic Buffett-style filters
            if pe and roe and debt_equity:
                if pe < 20 and roe > 0.15 and debt_equity < 1.0:
                    picks.append(ticker)

        except Exception:
            continue

    # If nothing passed the filters, return known Buffett picks filtered by universe
    if not picks:
        picks = [t for t in known_buffett_holdings if t in tickers]

    return picks