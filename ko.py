
# market_report.py
# Python script to generate a daily market report for:
# - Top 3 US Indices: Dow Jones, S&P 500, NASDAQ 100
# - Most actively traded stocks (by volume)
# - Most actively traded options (by volume)
#
# Uses yfinance for data fetching
# Requires: pip install yfinance pandas

import yfinance as yf
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

def get_index_data():
    """Fetch current data for major US indices"""
    indices = {
        '^DJI': 'Dow Jones Industrial Average',
        '^GSPC': 'S&P 500',
        '^NDX': 'NASDAQ 100'
    }
    
    print("=== MAJOR US INDICES ===\n")
    print(f"{'Index':<35} {'Close':>12} {'Change':>10} {'% Change':>10} {'Volume':>12}")
    print("-" * 75)
    
    for symbol, name in indices.items():
        try:
            ticker = yf.Tiscker(symbol)
            hist = ticker.history(period="2d")
            if len(hist) < 2:
                continue
                
            close = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            change = close - prev_close
            pct_change = (change / prev_close) * 100
            volume = hist['Volume'].iloc[-1]
            
            print(f"{name:<35} {close:>12,.2f} {change:>+10,.2f} {pct_change:>+9.2f}% {volume:>12,.0f}")
            
        except Exception as e:
            print(f"{name:<35} {'ERROR':>12}")
    
    print()

def get_most_active_stocks(limit=10):
    """Fetch most actively traded stocks from Yahoo Finance"""
    print(f"=== TOP {limit} MOST ACTIVELY TRADED STOCKS (BY VOLUME) ===\n")
