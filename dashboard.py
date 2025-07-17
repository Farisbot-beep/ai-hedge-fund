import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load vote data from file
@st.cache_data
def load_votes():
    try:
        df = pd.read_csv("data/votes.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Ticker", "Agent"])
    
# Display title
st.title("📊 AI Hedge Fund Dashboard")
st.markdown("### 🧠 Multi-Agent Consensus & Voting Insights")

# Load votes
votes_df = load_votes()

if votes_df.empty:
    st.warning("No vote data found. Run main.py to generate votes.")
    st.stop()

# Count votes per ticker
vote_counts = votes_df.groupby("Ticker").Agent.count().reset_index()
vote_counts.columns = ["Ticker", "Votes"]
vote_counts = vote_counts.sort_values("Votes", ascending=False)

# Merge to show which agents voted for each stock
overlap_df = votes_df.groupby("Ticker")["Agent"].apply(list).reset_index()
merged_df = pd.merge(vote_counts, overlap_df, on="Ticker")

# Filter by minimum votes
min_votes = st.slider("🔢 Minimum votes to show", 1, votes_df["Agent"].nunique(), 2)
filtered_df = merged_df[merged_df["Votes"] >= min_votes]

# Display table
st.markdown("### 🏆 Top Consensus Picks")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Bar plot of vote counts
st.markdown("### 📈 Vote Count Chart")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_df, x="Ticker", y="Votes", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Optional: Show full matrix (tickers x agents)
st.markdown("### 🔍 Agent-Ticker Matrix (Who Voted What)")
matrix_df = pd.crosstab(votes_df["Ticker"], votes_df["Agent"])
st.dataframe(matrix_df, use_container_width=True)