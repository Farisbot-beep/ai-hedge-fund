import yfinance as yf

def get_dividend_scores(stock_list):
    """
    Returns a dictionary of {symbol: dividend_score} for stocks with dividend yield
    """
    picks = {}

    for symbol in stock_list:
        try:
            info = yf.Ticker(symbol).info
            dividend_yield = info.get('dividendYield')

            if dividend_yield:
                if dividend_yield >= 0.05:
                    score = 5
                elif dividend_yield >= 0.04:
                    score = 4
                elif dividend_yield >= 0.03:
                    score = 3
                elif dividend_yield >= 0.02:
                    score = 2
                else:
                    score = 1
                picks[symbol] = score
        except:
            continue

    return picks