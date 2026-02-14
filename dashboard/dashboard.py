import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")

st.title("📊 Trader Performance vs Market Sentiment Dashboard")

fear = pd.read_csv("C:\\Trader_Sentiment_Analysis\\data\\fear_greed.csv")
trader = pd.read_csv("C:\\Trader_Sentiment_Analysis\\data\\trader_data.csv")

fear['date'] = pd.to_datetime(fear['date'], dayfirst=True)
trader['Timestamp IST'] = pd.to_datetime(trader['Timestamp IST'], errors='coerce')
trader['date'] = pd.to_datetime(trader['Timestamp IST'].dt.date)

daily = trader.groupby(['date','Account'], as_index=False).agg({
    'Closed PnL':'sum',
    'Size USD':'mean',
    'Execution Price':'count'
})

daily.rename(columns={'Execution Price':'num_trades'}, inplace=True)

df = daily.merge(fear[['date','classification']], on='date', how='left')

st.sidebar.header("Filters")
sentiment_filter = st.sidebar.selectbox(
    "Select Sentiment",
    ["All","Fear","Greed"]
)

if sentiment_filter != "All":
    df = df[df['classification']==sentiment_filter]

st.subheader("Dataset Overview")
col1,col2,col3 = st.columns(3)

col1.metric("Total Trades", len(trader))
col2.metric("Total Traders", trader['Account'].nunique())
col3.metric("Total PnL", round(trader['Closed PnL'].sum(),2))

st.subheader("PnL Distribution by Sentiment")

fig1, ax1 = plt.subplots(figsize=(7,3))
sns.boxplot(x='classification', y='Closed PnL', data=df, ax=ax1)
st.pyplot(fig1, use_container_width=False)

st.subheader("Trade Frequency by Sentiment")

fig2, ax2 = plt.subplots(figsize=(7,3))
sns.barplot(x='classification', y='num_trades', data=df, ax=ax2)
st.pyplot(fig2, use_container_width=False)


st.subheader("Average Trade Size by Sentiment")
fig3, ax3 = plt.subplots(figsize=(7,3))
sns.barplot(x='classification', y='Size USD', data=df, ax=ax3)
st.pyplot(fig3, use_container_width=False)

st.success("Dashboard shows how trader behavior changes with market sentiment.")
