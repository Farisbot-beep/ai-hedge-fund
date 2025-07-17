import yfinance as yf

# Optionally include tickers from external files or APIs here
SP500_TICKERS = [
    # A sample of S&P 500 tickers (you can replace this with full list from file or API)
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "JNJ", "XOM",
    "V", "PG", "UNH", "HD", "MA", "PFE", "MRK", "KO", "PEP", "BAC", "CVX",
    "INTC", "WMT", "DIS", "T", "CSCO", "VZ", "ADBE", "NFLX", "CRM", "ABT", "LLY",
    # ... extend this to full ~500 tickers
]

def is_valid_ticker(ticker):
    """Check if a ticker has recent price data"""
    try:
        data = yf.download(ticker, period="5d", progress=False)
        return not data.empty
    except:
        return False

def get_custom_universe():
    """Load and return a list of valid stock tickers"""
    print("🧠 Validating tickers...")
    universe = []

    for ticker in SP500_TICKERS:
        if is_valid_ticker(ticker):
            universe.append(ticker)

    return universe