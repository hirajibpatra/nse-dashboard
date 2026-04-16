import streamlit as st
import pandas as pd
import time
from datetime import datetime
from scraper import get_market_data

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
    .heatmap-positive { background-color: rgba(34, 197, 94, 0.3); }
    .heatmap-negative { background-color: rgba(239, 68, 68, 0.3); }
</style>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None

def refresh_data():
    with st.spinner('Fetching latest data...'):
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
    refresh_interval = st.slider("Refresh (seconds)", 30, 300, 60)
    if st.button("🔄 Refresh", type="primary"):
        refresh_data()
    st.markdown("---")
    st.markdown(f"**Last:** {st.session_state.last_refresh.strftime('%H:%M:%S') if st.session_state.last_refresh else 'Never'}")
    if auto_refresh:
        elapsed = (datetime.now() - st.session_state.last_refresh).seconds if st.session_state.last_refresh else 0
        st.markdown(f"**Next:** {max(0, refresh_interval - elapsed)}s")

if st.session_state.data is None:
    refresh_data()

tabs = st.tabs([
    "📊 Indices", "🗺️ Heatmap", "📈 Thematic", "🏭 Sectoral", 
    "🔍 Stock Search", "🏆 Category Movers", "🤖 AI Picks", "💰 FII/DII"
])

with tabs[0]:
    st.subheader("Live Market Indices")
    if st.session_state.data.get('indices'):
        df = pd.DataFrame(st.session_state.data['indices'])
        cols = st.columns(3)
        for idx, row in df.iterrows():
            if idx < len(cols):
                with cols[idx % 3]:
                    st.metric(label=row['Symbol'], value=f"{row['Value']:,.2f}", delta=f"{row['Change %']:+.2f}%")
        st.dataframe(df, use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("Market Heatmap")
    if st.session_state.data.get('indices'):
        df = pd.DataFrame(st.session_state.data['indices'])
        for _, row in df.iterrows():
            color = "#22c55e" if row['Change %'] > 0 else "#ef4444"
            st.markdown(f"""
                <div style="background-color: {color}20; padding: 10px; margin: 5px; border-radius: 5px; display: inline-block;">
                    <b>{row['Symbol']}</b><br>
                    {row['Value']:,.2f}<br>
                    <span style="color: {color};">{row['Change %']:+.2f}%</span>
                </div>
            """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Thematic Indices")
    if st.session_state.data.get('thematic'):
        df = pd.DataFrame(st.session_state.data['thematic'])
        st.dataframe(df, use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Sectoral Indices")
    if st.session_state.data.get('sectoral'):
        df = pd.DataFrame(st.session_state.data['sectoral'])
        st.dataframe(df, use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Stock Search")
    symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE, TCS, INFY)")
    if symbol:
        from scraper import NSEScraper
        scraper = NSEScraper()
        result = scraper.search_stock(symbol)
        if result:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Price", f"₹{result['Price']}")
            c2.metric("Change", f"{result['Change']:+.2f}")
            c3.metric("Change %", f"{result['Change %']:+.2f}%")
            c4.metric("Volume", f"{result['Volume']:,}")
            c1, c2 = st.columns(2)
            c1.metric("High", f"₹{result['High']}")
            c2.metric("Low", f"₹{result['Low']}")
        else:
            st.warning("Stock not found")

with tabs[5]:
    st.subheader("Category-wise Gainers/Losers")
    if st.session_state.data.get('category_movers'):
        categories = st.selectbox("Select Category", list(st.session_state.data['category_movers'].keys()))
        cat_data = st.session_state.data['category_movers'][categories]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🟢 Gainers")
            if cat_data.get('gainers'):
                st.dataframe(pd.DataFrame(cat_data['gainers']), use_container_width=True, hide_index=True)
        with col2:
            st.markdown("### 🔴 Losers")
            if cat_data.get('losers'):
                st.dataframe(pd.DataFrame(cat_data['losers']), use_container_width=True, hide_index=True)

with tabs[6]:
    st.subheader("🤖 AI Recommendations")
    if st.session_state.data.get('ai_recommendations'):
        recs = st.session_state.data['ai_recommendations']
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📈 Upside Opportunities")
            if recs.get('upside'):
                for rec in recs['upside']:
                    st.success(f"**{rec['Symbol']}** - ₹{rec['Price']} | Upside: {rec['Upside %']}% | {rec['Reason']}")
        with col2:
            st.markdown("### 📉 Downside Watch")
            if recs.get('downside'):
                for rec in recs['downside']:
                    st.error(f"**{rec['Symbol']}** - ₹{rec['Price']} | Risk: {rec['Downside %']}% | {rec['Reason']}")

with tabs[7]:
    st.subheader("FII/DII Data")
    if st.session_state.data.get('fii_dii'):
        fii = st.session_state.data['fii_dii']
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("FII Buy", f"₹{fii['FII']['Buy']} Cr")
        c2.metric("FII Sell", f"₹{fii['FII']['Sell']} Cr")
        c3.metric("FII Net", f"₹{fii['FII']['Net']} Cr", delta=fii['FII']['Net'])
        c4.metric("Date", fii.get('Date', 'N/A'))
        c1, c2, c3 = st.columns(3)
        c1.metric("DII Buy", f"₹{fii['DII']['Buy']} Cr")
        c2.metric("DII Sell", f"₹{fii['DII']['Sell']} Cr")
        c3.metric("DII Net", f"₹{fii['DII']['Net']} Cr", delta=fii['DII']['Net'])

if auto_refresh:
    time.sleep(1)
    st.rerun()
