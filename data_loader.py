import pandas as pd

def get_spy_holdings():
    """
    Returns a list of S&P 500 stock tickers from a public GitHub CSV
    """
    try:
        url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
        df = pd.read_csv(url)
        return df['Symbol'].tolist()
    except Exception as e:
        print("❌ Error loading SPY tickers:", e)
        return []

def get_custom_universe(limit=100):
    """
    Returns the top N stocks from the SPY list
    """
    return get_spy_holdings()[:limit]
