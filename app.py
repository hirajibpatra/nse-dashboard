import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_market_data, NSEScraper
import time

st.set_page_config(
    page_title="NSE India Stock Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 8px 8px 0px 0px; padding: 10px 20px; color: #e2e8f0; }
    .stTabs [aria-selected="true"] { background-color: #22c55e; color: white; }
    div[data-testid="stDataFrame"] { background-color: #1e293b; }
    .positive { color: #22c55e; font-weight: bold; }
    .negative { color: #ef4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None
if 'auto_refresh_count' not in st.session_state:
    st.session_state.auto_refresh_count = 0

def refresh_data():
    try:
        st.session_state.data = get_market_data()
        st.session_state.last_refresh = datetime.now()
    except Exception as e:
        st.error(f"Error: {e}")

st.title("📈 NSE India Stock Dashboard")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Controls")
    auto_refresh = st.toggle("Auto-refresh", value=True)
    refresh_interval = st.slider("Refresh interval (seconds)", 30, 300, 60)
    if st.button("🔄 Refresh Now", type="primary"):
        refresh_data()
    st.markdown("---")
    if st.session_state.last_refresh:
        st.markdown(f"**Last refresh:** {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    else:
        st.markdown("**Last refresh:** Never")

if st.session_state.data is None:
    refresh_data()

tabs = st.tabs([
    "📊 Indices", "🗺️ Heatmap", "📈 Thematic", "🏭 Sectoral", 
    "🔍 Stock Search", "🏆 Category Movers", "🤖 AI Picks", "💰 FII/DII"
])

with tabs[0]:
    st.subheader("Live Market Indices")
    data = st.session_state.data.get('indices', []) if st.session_state.data else []
    if data:
        df = pd.DataFrame(data)
        cols = st.columns(4)
        for idx, row in df.head(8).iterrows():
            with cols[idx % 4]:
                delta_color = "normal" if row['Change %'] >= 0 else "inverse"
                st.metric(label=row['Symbol'], value=f"₹{row['Value']:,.2f}", delta=f"{row['Change %']:+.2f}%", delta_color=delta_color)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No data available")

with tabs[1]:
    st.subheader("Market Heatmap")
    data = st.session_state.data.get('indices', []) if st.session_state.data else []
    if data:
        cols = st.columns(4)
        for idx, row in enumerate(data):
            color = "#22c55e" if row['Change %'] > 0 else "#ef4444"
            with cols[idx % 4]:
                st.markdown(f"""
                <div style="background-color: {color}20; padding: 15px; border-radius: 8px; margin: 5px; text-align: center;">
                    <b style="font-size: 16px;">{row['Symbol']}</b><br>
                    <span style="font-size: 18px;">₹{row['Value']:,.2f}</span><br>
                    <span style="color: {color}; font-size: 14px;">{row['Change %']:+.2f}%</span>
                </div>
                """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Thematic Indices")
    data = st.session_state.data.get('thematic', []) if st.session_state.data else []
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No thematic data available")

with tabs[3]:
    st.subheader("Sectoral Indices")
    data = st.session_state.data.get('sectoral', []) if st.session_state.data else []
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No sectoral data available")

with tabs[4]:
    st.subheader("Stock Search")
    symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE, TCS, INFY)")
    if symbol:
        scraper = NSEScraper()
        result = scraper.search_stock(symbol)
        if result:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Price", f"₹{result['Price']}")
            c2.metric("Change", f"₹{result['Change']:+.2f}")
            c3.metric("Change %", f"{result['Change %']:+.2f}%")
            c4.metric("Volume", f"{result['Volume']:,}")
            
            c5, c6 = st.columns(2)
            c5.metric("High", f"₹{result['High']}")
            c6.metric("Low", f"₹{result['Low']}")
            
            st.info(f"Open: ₹{result['Open']}")
        else:
            st.warning(f"Stock '{symbol}' not found. Try a valid NSE symbol like RELIANCE, TCS, INFY")

with tabs[5]:
    st.subheader("Category-wise Gainers/Losers")
    data = st.session_state.data.get('category_movers', {}) if st.session_state.data else {}
    if data:
        categories = list(data.keys())
        category = st.selectbox("Select Category", categories)
        cat_data = data[category]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🟢 Gainers")
            if cat_data.get('gainers'):
                st.dataframe(pd.DataFrame(cat_data['gainers']), use_container_width=True, hide_index=True)
            else:
                st.info("No gainers")
        with col2:
            st.markdown("### 🔴 Losers")
            if cat_data.get('losers'):
                st.dataframe(pd.DataFrame(cat_data['losers']), use_container_width=True, hide_index=True)
            else:
                st.info("No losers")
    else:
        st.warning("No category data available")

with tabs[6]:
    st.subheader("AI Trading Recommendations")
    data = st.session_state.data.get('ai_recommendations', {}) if st.session_state.data else {}
    if data:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📈 Upside Opportunities")
            if data.get('upside'):
                for rec in data['upside']:
                    st.success(f"**{rec['Symbol']}** - ₹{rec['Price']} | Upside: {rec['Upside %']}% | Vol Ratio: {rec['Volume Ratio']}x")
            else:
                st.info("No upside opportunities")
        with col2:
            st.markdown("### 📉 Downside Watch")
            if data.get('downside'):
                for rec in data['downside']:
                    st.error(f"**{rec['Symbol']}** - ₹{rec['Price']} | Risk: {rec['Downside %']}% | Vol Ratio: {rec['Volume Ratio']}x")
            else:
                st.info("No downside watch")
    else:
        st.warning("No AI recommendations available")

with tabs[7]:
    st.subheader("FII/DII Data")
    data = st.session_state.data.get('fii_dii', {}) if st.session_state.data else {}
    if data:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("FII Buy", f"₹{data['FII']['Buy']} Cr")
        c2.metric("FII Sell", f"₹{data['FII']['Sell']} Cr")
        fii_net = data['FII']['Net']
        c3.metric("FII Net", f"₹{fii_net} Cr", delta=f"₹{fii_net} Cr", delta_color="normal" if fii_net >= 0 else "inverse")
        c4.metric("Date", data.get('Date', 'N/A'))
        
        c5, c6, c7 = st.columns(3)
        c5.metric("DII Buy", f"₹{data['DII']['Buy']} Cr")
        c6.metric("DII Sell", f"₹{data['DII']['Sell']} Cr")
        dii_net = data['DII']['Net']
        c7.metric("DII Net", f"₹{dii_net} Cr", delta=f"₹{dii_net} Cr", delta_color="normal" if dii_net >= 0 else "inverse")
    else:
        st.warning("No FII/DII data available")

if auto_refresh:
    st.session_state.auto_refresh_count += 1
    if st.session_state.auto_refresh_count >= refresh_interval:
        st.session_state.auto_refresh_count = 0
        refresh_data()
    time.sleep(1)
    st.rerun()