import yfinance as yf

def get_gold_price():
    gold = yf.Ticker("GC=F")  # Gold Futures

    # Try to get 1-minute data for last 5 days
    data = gold.history(period="5d", interval="1m")
    if not data.empty:
        return round(data['Close'].dropna().iloc[-1], 2)

    # Fallback: get latest available daily close (e.g., Friday)
    fallback = gold.history(period="1mo", interval="1d")
    if not fallback.empty:
        return round(fallback['Close'].dropna().iloc[-1], 2)

    # If nothing works
    return None