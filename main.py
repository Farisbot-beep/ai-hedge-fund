from data_loader import get_custom_universe as get_stock_universe

from agents.buffett_agent import get_buffett_recommendations
from agents.sentiment_agent import get_sentiment_recommendations
from agents.dividend_agent import get_dividend_scores
from agents.technical_agent import get_technical_picks
from agents.growth_agent import get_growth_picks
from agents.value_agent import get_value_picks
from agents.momentum_agent import get_momentum_picks
from agents.etf_agent import get_halal_etfs
from agents.halal_agent import filter_halal

from utils import execute_rebalance, send_telegram_message

print("🚀 Running AI Hedge Fund...\n")

# 1. Load & filter universe
universe = get_stock_universe()
print(f"📦 Universe loaded: {len(universe)} stocks")

halal_universe = filter_halal(universe)
print(f"🕌 Halal-compliant stocks: {len(halal_universe)}")

# 2. Get agent recommendations
print("🧠 Running agents...\n")

buffett = get_buffett_recommendations(halal_universe)
print(f"📊 Buffett Picks: {buffett}")

sentiment = get_sentiment_recommendations(halal_universe)
print(f"💬 Sentiment Picks: {sentiment}")

dividends = get_dividend_scores(halal_universe)
print(f"🪙 Dividend Picks: {dividends}")

technical = get_technical_picks(halal_universe)
print(f"📉 Technical Picks: {technical}")

growth = get_growth_picks(halal_universe)
print(f"📈 Growth Picks: {growth}")

value = get_value_picks(halal_universe)
print(f"💰 Value Picks: {value}")

momentum = get_momentum_picks(halal_universe)
print(f"⚡ Momentum Picks: {momentum}")

etfs = get_halal_etfs()
print(f"📦 Halal ETFs: {etfs}")

# 3. Voting system
agent_votes = {}
agents = [buffett, sentiment, dividends, technical, growth, value, momentum, etfs]

for agent_output in agents:
    for symbol in agent_output:
        agent_votes[symbol] = agent_votes.get(symbol, 0) + 1

# 4. Consensus (2+ votes)
consensus = [symbol for symbol, votes in agent_votes.items() if votes >= 2]

print(f"\n🤝 Consensus Picks: {consensus if consensus else 'None'}")

# 5. Rebalance + Notify
if consensus:
    send_telegram_message(f"🤖 Rebalancing with: {', '.join(consensus)}")
    execute_rebalance(consensus)
else:
    send_telegram_message("⚠️ No consensus picks for this round.")