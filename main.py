from agents.buffett_agent import get_buffett_recommendations
from agents.sentiment_agent import get_sentiment_recommendations
from agents.dividend_agent import get_dividend_scores
from agents.technical_agent import get_technical_picks
from agents.growth_agent import get_growth_picks
from agents.halal_agent import filter_halal

from utils import execute_trade, get_portfolio_summary, send_telegram_message
from data_loader import get_custom_universe

def run_hedge_fund():
    print("🚀 Running AI Hedge Fund...\n")

    # === Load dynamic stock universe ===
    universe = get_custom_universe(limit=100)
    print(f"📦 Universe loaded: {len(universe)} stocks")

    # === Agent recommendations ===
    buffett = get_buffett_recommendations()
    sentiment = get_sentiment_recommendations()
    dividends = get_dividend_scores(universe)
    technical = get_technical_picks(universe)
    growth = get_growth_picks(universe)

    print("📊 Buffett Picks:", buffett)
    print("💬 Sentiment Picks:", sentiment)
    print("🪙 Dividend Picks:", list(dividends.keys()))
    print("📉 Technical Picks:", technical)
    print("📈 Growth Picks:", growth)

    # === Voting System: score stocks across agents ===
    vote_count = {}

    def add_votes(symbols, weight=1):
        for symbol in symbols:
            vote_count[symbol] = vote_count.get(symbol, 0) + weight

    add_votes(buffett, weight=1)
    add_votes(sentiment, weight=1)
    add_votes(dividends.keys(), weight=1)
    add_votes(technical, weight=1)
    add_votes(growth, weight=1)

    # Select stocks with 2 or more votes
    consensus = {symbol for symbol, votes in vote_count.items() if votes >= 2}
    print("\n🗳️ Voted Consensus Picks (3+ votes):", consensus)

    if not consensus:
        print("⚠️ No consensus picks between agents this round.")
        return

    # === Apply Halal Filter ===
    halal_consensus = filter_halal(consensus)
    print("\n🕌 Halal-Filtered Consensus Picks:", halal_consensus)

    if not halal_consensus:
        print("⚠️ No halal stocks in consensus.")
        return

    # === Execute Paper Trades ===
    print("\n📈 Executing Paper Trades...")
    for stock in halal_consensus:
        score = dividends.get(stock, "N/A")
        print(f"➡️ Buying 1 share of {stock} (Dividend Score: {score})")
        execute_trade(stock, qty=1, side='buy')

    # === Send Telegram Alert ===
    alert = "📢 AI Hedge Fund Picks:\n" + '\n'.join([f"- {s}" for s in halal_consensus])
    send_telegram_message(alert)

    # === Portfolio Summary ===
    print("\n📊 Portfolio Summary:")
    portfolio = get_portfolio_summary()
    for item in portfolio:
        print(
            f"{item['Symbol']}: {item['Quantity']} shares | Buy @ ${item['Buy Price']} → Now @ ${item['Current Price']} | Change: {item['Change %']}%"
        )

if __name__ == "__main__":
    run_hedge_fund()