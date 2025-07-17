import yfinance as yf

def get_growth_picks(stock_list):
    """
    Returns a list of stocks with EPS and revenue growth > 10%
    """
    picks = []

    for symbol in stock_list:
        try:
            info = yf.Ticker(symbol).info
            eps_growth = info.get('earningsQuarterlyGrowth', 0)
            revenue_growth = info.get('revenueGrowth', 0)

            if eps_growth and revenue_growth and eps_growth > 0.1 and revenue_growth > 0.1:
                picks.append(symbol)
        except:
            continue

    return picks