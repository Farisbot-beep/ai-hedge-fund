halal_stocks = ['AAPL', 'MSFT', 'TSLA', 'ADBE', 'O', 'T', 'JNJ', 'PG']

def filter_halal(stocks):
    return [s for s in stocks if s in halal_stocks]