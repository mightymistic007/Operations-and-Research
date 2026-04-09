import yfinance as yf
import pandas as pd
import numpy as np
import os
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns

# Global Configuration
STOCK_POOL = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN', 'META', 'NVDA', 'BRK-B']

def get_recommended_tickers(amount):
    if amount < 20000: return STOCK_POOL[:2]
    elif 20000 <= amount < 100000: return STOCK_POOL[:4]
    else: return STOCK_POOL[:6]

def generate_investment_plan(amount, weights, mu, S, var_amt):
    """
    Prints a detailed professional investment report to the console.
    """
    print("\n" + "="*50)
    print(f" INVESTMENT STRATEGY REPORT (Capital: ₹{amount:,})")
    print("="*50)
    print(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Risk Profile: 95% Daily Value-at-Risk is ₹{var_amt:,}")
    print("-" * 50)
    print(f"{'Ticker':<10} {'Allocation (₹)':<18} {'Weight (%)':<12} {'Exp. Return'}")
    
    for ticker, weight in weights.items():
        alloc = amount * weight
        ret = mu[ticker] * 100
        print(f"{ticker:<10} ₹{alloc:<17,.2f} {weight*100:<11.2f}% {ret:>10.2f}%")
    
    print("-" * 50)
    print("STRATEGY NOTES:")
    if len(weights) <= 2:
        print("- Focus: High-conviction growth for small capital.")
    elif len(weights) >= 5:
        print("- Focus: Institutional-grade diversification to minimize volatility.")
    print("=" * 50 + "\n")

def get_optimal_weights(tickers, total_inv):
    if not tickers: return {}, 0, 0, 0, [], [], pd.DataFrame()
    
    # 1. FETCH & CLEAN DATA
    raw_data = yf.download(tickers, period="2y", progress=False)
    if raw_data.empty: return {}, 0, 0, 0, [], [], pd.DataFrame()
    raw_data.to_csv("market_raw_data.csv")

    try:
        if isinstance(raw_data.columns, pd.MultiIndex):
            col = 'Adj Close' if 'Adj Close' in raw_data.columns.levels[0] else 'Close'
            data = raw_data.xs(col, axis=1, level=0)
        else:
            data = raw_data['Adj Close'] if 'Adj Close' in raw_data.columns else raw_data['Close']
    except: return {}, 0, 0, 0, [], [], pd.DataFrame()

    data = data.dropna().ffill()

    # 2. STATISTICAL MODELING
    mu = expected_returns.mean_historical_return(data)
    S = risk_models.sample_cov(data)

    # 3. OPTIMIZATION WITH ERROR HANDLING
    try:
        ef = EfficientFrontier(mu, S)
        # Solve first
        ef.max_sharpe() 
        # Then clean
        weights = ef.clean_weights()
    except Exception:
        # Fallback to equal weighting if optimization fails
        weights = {t: 1.0/len(tickers) for t in tickers}

    # 4. RISK CALCULATION
    w_arr = np.array(list(weights.values()))
    port_vol = np.sqrt(np.dot(w_arr.T, np.dot(S, w_arr)))
    port_ret = np.sum(mu * w_arr)
    var_95 = total_inv * (port_vol * 1.645 / np.sqrt(252))
    
    # Generate the Console Plan
    generate_investment_plan(total_inv, weights, mu, S, round(var_95, 2))

    # 5. ASSET DATAFRAME FOR APP
    asset_data = pd.DataFrame({
        'Ticker': list(weights.keys()),
        'Weight': [weights[t] for t in weights.keys()],
        'Allocation': [weights[t] * total_inv for t in weights.keys()],
        'Exp_Return': [mu[t] * 100 for t in weights.keys()],
        'Volatility': [np.sqrt(S.loc[t, t]) * 100 for t in weights.keys()]
    })
    
    stds, rems = [], []
    for _ in range(300):
        w = np.random.random(len(data.columns))
        w /= np.sum(w)
        rems.append(np.dot(w, mu))
        stds.append(np.sqrt(np.dot(w.T, np.dot(S, w))))
        
    return weights, round(port_ret*100, 2), round(port_vol*100, 2), round(var_95, 2), stds, rems, asset_data

def log_transaction(data_dict):
    df = pd.DataFrame([data_dict])
    if not os.path.isfile('portfolio_history.csv'):
        df.to_csv('portfolio_history.csv', index=False)
    else:
        df.to_csv('portfolio_history.csv', mode='a', header=False, index=False)

# --- SELF-TEST BLOCK ---
# This allows you to run main.py directly to see the plan without the Streamlit app
if __name__ == "__main__":
    test_amount = 50000 
    test_tickers = get_recommended_tickers(test_amount)
    get_optimal_weights(test_tickers, test_amount)