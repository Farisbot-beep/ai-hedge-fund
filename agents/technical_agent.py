import yfinance as yf

def calculate_rsi(prices, period=14):
    delta = prices.diff().dropna()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_technical_picks(stock_list):
    """
    Returns a list of stocks where RSI < 30 (oversold condition)
    """
    picks = []

    for symbol in stock_list:
        try:
            data = yf.Ticker(symbol).history(period='30d')
            if data.empty or len(data) < 15:
                continue

            rsi = calculate_rsi(data['Close'])
            if not rsi.empty and rsi.iloc[-1] < 30:
                picks.append(symbol)
        except:
            continue

    return picks