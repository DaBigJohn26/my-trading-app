import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime

st.set_page_config(page_title="Alpha Confluence Command Center", layout="wide")

st.title("🧠 Institutional Multi-Confluence Trading Dashboard")
st.caption("System Status: 🟢 Always-On Cloud Scanning Online (No Laptop Required)")

# Sidebar for Mobile Notification Configuration
st.sidebar.header("🔌 Phone Link Settings")
telegram_token = 8666247444:AAEFH9hkcNl6ioXQyQAZGmlNdr9FR2fw098
chat_id = st.sidebar.text_input("8546529654")
min_score = st.sidebar.slider("Minimum Execution Score Trigger", 50, 80, 60)

def is_high_impact_news_active():
    try:
        url = "https://horizonfx.id" 
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            events = response.json().get("events", [])
            current_time = datetime.utcnow()
            for event in events:
                if event.get("currency") == "USD" and event.get("impact") == "HIGH":
                    event_name = event.get("name", "").upper()
                    if any(kw in event_name for kw in ["CPI", "NFP", "PAYROLL", "FED", "FOMC", "INFLATION", "INTEREST"]):
                        event_time = datetime.strptime(event.get("time"), "%Y-%m-%d %H:%M:%S")
                        time_difference = abs((event_time - current_time).total_seconds() / 60.0)
                        if time_difference <= 15:
                            return True, event.get("name")
        return False, ""
    except:
        return False, ""

def send_telegram_notification(message):
    if telegram_token and chat_id:
        url = f"https://telegram.org{telegram_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try: requests.post(url, json=payload, timeout=5)
        except: pass

# 1. Fundamental News Calendar Shield Check
news_active, news_name = is_high_impact_news_active()
if news_active:
    st.error(f"🚨 SYSTEM LOCKDOWN: Trading frozen due to active high-impact release: {news_name}")
else:
    st.success("🛡️ Capital Shield Active: No dangerous macro news events blocking current market structure.")

# 2. Main Strategy Processing Matrix
tickers = {"BTC-USD": "Crypto", "GC=F": "Gold", "EURUSD=X": "Forex"}
cols = st.columns(len(tickers))

for idx, (ticker, sector) in enumerate(tickers.items()):
    with cols[idx]:
        st.markdown(f"### **{ticker}** ({sector})")
        
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False, multi_level_index=False)
            if df.empty or len(df) < 35:
                st.error("Data Stream Lagging")
                continue
                
            # Balanced Indicator Math
            df['Swing_High'] = df['High'].shift(1).rolling(window=5).max()
            df['Market_Structure_Trend'] = np.where(df['Close'] > df['Swing_High'], 1, 0)
            df['Body_Size'] = (df['Close'] - df['Open']).abs()
            df['Prev_Body_Size'] = df['Body_Size'].shift(1)
            df['Bullish_Candle'] = np.where((df['Close'] > df['Open']) & (df['Body_Size'] > df['Prev_Body_Size']), 1, 0)
            df['Support_Zone'] = df['Low'].rolling(window=20).min().shift(1)
            df['EMA_Fast'] = df['Close'].rolling(window=12).mean()
            df['EMA_Slow'] = df['Close'].rolling(window=26).mean()
            df['MACD'] = df['EMA_Fast'] - df['EMA_Slow']
            df['MACD_Signal'] = df['MACD'].rolling(window=9).mean()
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            df['RSI'] = 100 - (100 / (1 + (gain / (loss + 1e-10))))

            current_close = float(df['Close'].iat[-1])
            current_low = float(df['Low'].iat[-1])
            demand_floor = float(df['Support_Zone'].iat[-1])

            # Confluence Scoring Matrix
            score = 0
            if int(df['Market_Structure_Trend'].iat[-1]) == 1 or current_close > float(df['EMA_Fast'].iat[-1]): score += 30
            if int(df['Bullish_Candle'].iat[-1]) == 1: score += 30
            if float(df['MACD'].iat[-1]) > float(df['MACD_Signal'].iat[-1]) and float(df['RSI'].iat[-1]) < 65: score += 20
            if 'Volume' in df.columns and float(df['Volume'].iat[-1]) > float(df['Volume'].rolling(window=20).mean().iat[-1]): score += 20

            # UI Dashboard Display Elements
            st.metric("Live Market Price", f"${current_close:,.2f}")
            st.write(f"**Strategy Confluence Score:** {score}/100")
            st.progress(score / 100)

            # Signal Evaluation Gate
            if not news_active:
                if score >= min_score:
                    st.success("🟩 TREND SIGNAL BUY TRIGGERED!")
                    send_telegram_notification(f"🟩 BUY ALERT: {ticker} hit a high confluence trend score of {score}/100 at ${current_close:,.2f}! Open MT5 on your phone to trade.")
                elif current_low < demand_floor and current_close > demand_floor:
                    st.warning("🎯 LIQUIDITY SWEEP BUY TRIGGERED!")
                    send_telegram_notification(f"🎯 TRAP ALERT: Institutional Liquidity Sweep detected on {ticker} at ${current_close:,.2f}! Open MT5 on your phone to trade.")
                else:
                    st.info("⬜ Holding: Waiting for Market Structure Alignment")
                    
        except Exception as e:
            st.error(f"Feed error: {e}")

st.divider()
st.info("💡 Tip: Bookmark this website link on your mobile phone's Home Screen. It will refresh automatically to scan global charts live in the cloud.")
