# DOYDOY HIGH-SPEED PRODUCTION CLOUD APP SYSTEM
import streamlit as st
import ccxt
import pandas as pd
import requests
import time

st.set_page_config(page_title="DOYDOY WARRIOR PORTAL", page_icon="⚔️", layout="centered")
st.title("⚔️ Warrior Trading Portal")
st.caption("Exclusive Algorithmic Portfolio Terminal Engine")

@st.cache_resource
def init_exchange_client():
    client = ccxt.binanceusdm({
        "apiKey": "0NksBQxcaJBLSlJfPjk3GuqMcFBMt952uBBT9OIbOqfx1gfipHlECthEyMn3tFoc",
        "secret": "gAwjxPB9pTUJ7fQRgQwKHwbAWD3VZBZk3WXBnIDzYPEFNlLJorIasj4MmtPlKu55",
        "enableRateLimit": True,
        "timeout": 30000,
        "options": {"defaultType": "future", "adjustForTimeDifference": True}
    })
    client.set_sandbox_mode(False)
    return client

exchange = init_exchange_client()

TELEGRAM_BOT_TOKEN = "8845314154:AAFfEjUzOcrZ0W_TFpkQF67BguCj6BW4gwo"
TELEGRAM_CHAT_ID = "6290617083"
LEVERAGE = 5
MAX_SIMULTANEOUS_POSITIONS = 3
MIN_SAFE_USDT_BALANCE = 10.0

st.header("📊 Live Position Monitor")

def fetch_portfolio_metrics():
    try:
        balances = exchange.fetch_balance()
        positions = balances["info"]["positions"]
        active_trades = []
        for pos in positions:
            amt = float(pos.get("positionAmt", 0))
            if amt != 0.0:
                active_trades.append({
                    "Symbol": pos.get("symbol"),
                    "Size": amt,
                    "Entry": float(pos.get("entryPrice", 0)),
                    "Mark": float(pos.get("markPrice", 0)),
                    "PnL (USDT)": float(pos.get("unrealizedProfit", 0)),
                    "Margin Mode": "Isolated"
                })
        free_margin = float(balances.get("USDT", {}).get("free", 0))
        return active_trades, free_margin
    except Exception as e:
        st.error(f"Network error loading balances: {str(e)}")
        return [], 0.0

running_trades, available_cash = fetch_portfolio_metrics()

col1, col2 = st.columns(2)
with col1: st.metric("Available Usable Margin", f"{round(available_cash, 2)} USDT")
with col2: st.metric("Active Portfolio Positions", f"{len(running_trades)} / {MAX_SIMULTANEOUS_POSITIONS}")

if running_trades:
    df_positions = pd.DataFrame(running_trades)
    st.dataframe(df_positions.style.format({"Size": "{:.4f}", "Entry": "{:.5f}", "Mark": "{:.5f}", "PnL (USDT)": "{:+.2f}"}))
else:
    st.info("⚡ System Hibernate. Account is currently vacant. Radar waiting to deploy positions.")

st.header("🕹️ Mobile Emergency Controls")
if st.button("🚨 FORCE EMERGENCY CLOSE ALL TRADES", use_container_width=True):
    with st.spinner("Executing structural panic sequence..."):
        try:
            for pos in running_trades:
                sym = pos["Symbol"]
                size = abs(pos["Size"])
                side = "sell" if pos["Size"] > 0 else "buy"
                exchange.create_order(sym, "MARKET", side, size)
            url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": "🚨 <b>[EMERGENCY PANIC]</b> Manual Emergency Close All executed from your Phone app.", "parse_mode": "HTML"}
            requests.post(url, json=payload, timeout=5)
            st.success("Wiped account clean! All active risk assets closed.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Panic route failed: {str(e)}")

st.header("📡 Radar Engine System Logs")
if "radar_active" not in st.session_state:
    st.session_state.radar_active = False

col_start, col_stop = st.columns(2)
with col_start:
    if st.button("🟢 Ignite App Radar", use_container_width=True):
        st.session_state.radar_active = True
with col_stop:
    if st.button("🛑 Pause App Radar", use_container_width=True):
        st.session_state.radar_active = False

if st.session_state.radar_active:
    st.success("📡 5-Second Velocity Polling Engine running inside cloud threads...")
else:
    st.info("💤 Standby Mode.")
