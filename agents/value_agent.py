import yfinance as yf

def get_value_picks(tickers):
    value_stocks = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            pe = info.get("trailingPE")
            pb = info.get("priceToBook")
            roe = info.get("returnOnEquity")

            if pe and pb and roe:
                if pe < 15 and pb < 1.5 and roe > 0.15:
                    value_stocks.append(ticker)
        except Exception:
            continue
    return value_stocks