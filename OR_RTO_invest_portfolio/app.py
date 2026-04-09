import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from main import get_optimal_weights, log_transaction, get_recommended_tickers
from datetime import datetime
import time
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Risk-Aware Advisor", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4250;
    }
    </style>
    """, unsafe_allow_html=True)

# --- USER INPUT SECTION ---
st.title("🛡️ AI-Powered Portfolio Risk Engine")
amount = st.number_input("Enter Investment Capital (₹)", min_value=1000, value=50000, step=5000)

# 1. Get Tickers and Expanded Math from Engine
TICKERS = get_recommended_tickers(amount)
# Note: Now receiving 'asset_df' from main.py
weights, ann_ret, ann_vol, var_amt, stds, rems, asset_df = get_optimal_weights(TICKERS, amount)

# --- TOP ROW PERFORMANCE METRICS ---
st.subheader("Executive Risk Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Expected Annual Return", f"{ann_ret}%")
m2.metric("Portfolio Volatility (Risk)", f"{ann_vol}%")
m3.metric("95% Value at Risk (Daily)", f"₹{var_amt:,.2f}")

# --- ANALYTICS TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Asset Analytics", "📈 Efficient Frontier", "📂 Raw Market Data"])

with tab1:
    st.subheader("Individual Company Performance vs. Risk")
    c1, c2 = st.columns([1, 1])
    
    with c1:
        # Donut chart for money distribution
        fig_pie = px.pie(asset_df, values='Allocation', names='Ticker', hole=0.4, 
                         title="How your ₹ is Distributed", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        # Side-by-Side Bar Chart: Return vs Risk per Stock
        fig_bar = go.Figure(data=[
            go.Bar(name='Exp. Return %', x=asset_df['Ticker'], y=asset_df['Exp_Return'], marker_color='#00CC96'),
            go.Bar(name='Volatility (Risk) %', x=asset_df['Ticker'], y=asset_df['Volatility'], marker_color='#EF553B')
        ])
        fig_bar.update_layout(title="Company Comparison: Profit vs. Risk", barmode='group', template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Modern Portfolio Theory Simulation")
    if stds and rems:
        fig_ef = px.scatter(x=stds, y=rems, labels={'x':'Volatility', 'y':'Return'}, 
                           title="Efficient Frontier (Possible Portfolios)", color=rems,
                           template="plotly_dark")
        st.plotly_chart(fig_ef, use_container_width=True)
    st.caption("Each dot represents a different possible mix of these stocks. The AI picks the best one.")

with tab3:
    st.subheader("Direct Feed from Yahoo Finance")
    if os.path.exists("market_raw_data.csv"):
        raw_display = pd.read_csv("market_raw_data.csv", index_col=0)
        st.write("Below is the historical 'Adjusted Close' data used for calculations:")
        st.dataframe(raw_display, use_container_width=True)
        
        # Download button for the user
        with open("market_raw_data.csv", "rb") as file:
            st.download_button(
                label="📥 Download Raw Market Data (CSV)",
                data=file,
                file_name=f"market_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("Market data will appear here once the first analysis is complete.")

# --- LIVE EXECUTION LOGIC ---
st.divider()
st.subheader("Live Market Tracker")

if 'latest_status' not in st.session_state:
    st.session_state.latest_status = None

log_btn = st.button("💾 Log Current Performance Snapshot")

placeholder = st.empty()

while True:
    with placeholder.container():
        raw_live = yf.download(TICKERS, period="3d", interval="1m")
        
        if not raw_live.empty:
            try:
                if isinstance(raw_live.columns, pd.MultiIndex):
                    col = 'Adj Close' if 'Adj Close' in raw_live.columns.levels[0] else 'Close'
                    live_data = raw_live.xs(col, axis=1, level=0).ffill().iloc[-1]
                else:
                    col = 'Adj Close' if 'Adj Close' in raw_live.columns else 'Close'
                    live_data = raw_live[col].ffill().iloc[-1]
                
                cols = st.columns(len(TICKERS))
                current_status = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                
                for i, ticker in enumerate(TICKERS):
                    w = weights.get(ticker, 0)
                    price = live_data[ticker]
                    stock_value = amount * w
                    current_status[f"{ticker}_price"] = round(price, 2)
                    
                    with cols[i]:
                        st.metric(ticker, f"₹{price:.2f}")
                        st.caption(f"Target Value: ₹{stock_value:,.0f}")
                        st.progress(float(w))

                st.session_state.latest_status = current_status
            except Exception as e:
                st.error(f"Live Update Error: {e}")

        # Show History Table
        if os.path.exists('portfolio_history.csv'):
            try:
                df_hist = pd.read_csv('portfolio_history.csv')
                st.subheader("📋 Execution Logs")
                st.dataframe(df_hist.tail(5), use_container_width=True)
            except:
                pass

    if log_btn and st.session_state.latest_status:
        log_transaction(st.session_state.latest_status)
        st.toast("Record saved!", icon="✅")

    time.sleep(15)