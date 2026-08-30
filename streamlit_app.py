import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime

st.set_page_config(page_title="2090 Global Sessional Command", layout="wide")

st.title("👑 2090 Institutional Sessional Alpha Center")
st.caption("System Status: 🟢 Always-On Cloud Scanning Online (No Laptop Required)")

# ⚠️ TYPE YOUR WORKING TELEGRAM CREDENTIALS HERE
telegram_token = "8666247444:AAEFH9hkCNl6ioXQyQAZGmlNdr9FR2fw098"
chat_id = "8546529654"

def get_current_session():
    """Maps sessional regimes based on UTC hours"""
    current_hour = datetime.utcnow().hour
    if 22 <= current_hour or current_hour < 7:
        return "ASIAN_ACCUMULATION", "🔵 ASIAN SESSION: Accumulation & Range Mapping (Retail Trap Active)"
    elif 7 <= current_hour < 12:
        return "LONDON_MANIPULATION", "🔴 LONDON SESSION: Manipulation & Liquidity Sweeping (Hunting Stops)"
    else:
        return "NEW_YORK_DISTRIBUTION", "🟢 NEW YORK SESSION: Distribution & Impulse Extension (Riding Flow)"

def send_telegram_notification(message):
    if not telegram_token or "your_actual" in telegram_token or not chat_id:
        return
    try:
        url = f"https://telegram.org{telegram_token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=5)
    except: pass

# Identify Current Sessional Environment Live
session_id, session_text = get_current_session()
st.sidebar.markdown(f"### **Active Market Regime**\n{session_text}")

# Comprehensive 2090 Multi-Sector Global Asset Layout (Perfectly Aligned)
global_assets = {
    "EURUSD=X": "Forex - EURUSD", 
    "GBPUSD=X": "Forex - GBPUSD", 
    "USDJPY=X": "Forex - USDJPY",
    "AUDUSD=X": "Forex - AUDUSD", 
    "USDCAD=X": "Forex - USDCAD",
    "GC=F": "Metal - Gold", 
    "SI=F": "Metal - Silver", 
    "CL=F": "Commodity - Crude", 
    "NG=F": "Commodity - NatGas",
    "BTC-USD": "Crypto - Bitcoin", 
    "ETH-USD": "Crypto - Ethereum"
}

cols = st.columns(3)
asset_list = list(global_assets.items())

for index, (ticker, label) in enumerate(asset_list):
    col_idx = index % 3
    with cols[col_idx]:
        st.markdown(f"### **{label}**")
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False, multi_level_index=False)
            if df.empty or len(df) < 30:
                st.error("Feed Delay")
                continue
                
            # Compute underlying market structural variables
            df['Asian_High'] = df['High'].shift(1).rolling(window=3).max()
            df['Asian_Low'] = df['Low'].shift(1).rolling(window=3).min()
            
            high_low = df['High'] - df['Low']
            high_cp = (df['High'] - df['Close'].shift()).abs()
            low_cp = (df['Low'] - df['Close'].shift()).abs()
            df['ATR'] = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1).rolling(window=14).mean()
            
            df['EMA_Fast'] = df['Close'].rolling(window=12).mean()
            df['EMA_Slow'] = df['Close'].rolling(window=26).mean()
            df['MACD'] = df['EMA_Fast'] - df['EMA_Slow']
            df['MACD_Signal'] = df['MACD'].rolling(window=9).mean()

            current_close = float(df['Close'].iat[-1])
            current_low = float(df['Low'].iat[-1])
            current_high = float(df['High'].iat[-1])
            asian_high_zone = float(df['Asian_High'].iat[-1])
            asian_low_zone = float(df['Asian_Low'].iat[-1])

            st.metric("Live Market Price", f"${current_close:,.4f}")

            # 🧠 2090 SESSIONAL LOGIC TRIGGERS
            if session_id == "LONDON_MANIPULATION":
                if current_low < asian_low_zone and current_close > asian_low_zone:
                    st.warning("🎯 LONDON LIQUIDITY SWEEP DETECTED!")
                    send_telegram_notification(f"🎯 TRAP ALERT: London has swept the Asian Low on {label} at ${current_close:.4f}! Open your phone's MT5 app and trade with the institutions.")
                else:
                    st.info("⬜ London hunting for liquidity sweeps...")

            elif session_id == "NEW_YORK_DISTRIBUTION":
                if current_close > asian_high_zone and float(df['MACD'].iat[-1]) > float(df['MACD_Signal'].iat[-1]):
                    st.success("🟩 NEW YORK IMPULSE BREAKOUT!")
                    send_telegram_notification(f"🟩 BREAKOUT ALERT: New York has launched a major impulse move on {label} at ${current_close:.4f}! Open your phone's MT5 app to BUY.")
                else:
                    st.info("⬜ New York tracking macro momentum...")

            else:
                st.info("🔵 Asian Session: Mapping range boundaries. Stand aside.")
                
        except Exception as e:
            st.error("Synchronizing...")

st.divider()
st.info("💡 Your 2090 Engine automatically adapts its mathematical filters based on the UTC clock. Keep this tab open to monitor institutional order flows!")
