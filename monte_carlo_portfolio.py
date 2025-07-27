#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Monte Carlo Portfolio Optimization with Real Stock Data
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Define stock tickers
assets = ['AAPL', 'MSFT', 'NVDA']
start_date = '2020-01-01'
end_date = '2024-12-31'

# Download historical adjusted close prices
data = yf.download(assets, start=start_date, end=end_date)['Close']

# Calculate daily returns
daily_returns = data.pct_change().dropna()

# Compute annualized mean returns and covariance matrix
mu = daily_returns.mean() * 252
cov_matrix = daily_returns.cov() * 252

# Monte Carlo simulation: generate random weights
def generate_weights(n_assets, n_portfolios, allow_shorts=False):
    weights = []
    for _ in range(n_portfolios):
        if allow_shorts:
            w = np.random.uniform(-1, 1, n_assets)
        else:
            w = np.random.uniform(0, 1, n_assets)
        w /= np.sum(w)
        weights.append(w)
    return np.array(weights)

# Function to compute portfolio return and risk
def portfolio_stats(weights, mu, cov_matrix):
    returns = weights @ mu.values
    risks = np.sqrt(np.einsum('ij,ji->i', weights @ cov_matrix.values, weights.T))
    return returns, risks

# Simulation parameters
n_assets = len(assets)
n_portfolios = 700

# Simulate both strategies
weights_long = generate_weights(n_assets, n_portfolios, allow_shorts=False)
weights_short = generate_weights(n_assets, n_portfolios, allow_shorts=True)

returns_long, risks_long = portfolio_stats(weights_long, mu, cov_matrix)
returns_short, risks_short = portfolio_stats(weights_short, mu, cov_matrix)

# Plot the simulation results
plt.figure(figsize=(10, 6))
plt.scatter(risks_long, returns_long, c='blue', label='Long Only', alpha=0.5)
plt.scatter(risks_short, returns_short, c='red', label='Long & Short', alpha=0.5)
plt.xlabel('Risk (Standard Deviation)')
plt.ylabel('Return (Mean)')
plt.title('Monte Carlo Portfolio Simulation with Real Data\nAAPL, MSFT, NVDA (2020-2024)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:




