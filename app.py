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
</style>
""", unsafe_allow_html=True)
if 'data' not in st.session_state:
    st.session_state.data = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None
def refresh_data():
    with st.spinner('Fetching latest data from NSE...'):
        try:
            st.session_state.data = get_market_data()
            st.session_state.last_refresh = datetime.now()
        except Exception as e:
            st.error(f"Error fetching data: {e}")
def color_change(val):
    try:
        num = float(str(val).replace('%', '').replace(',', ''))
        return "🟢" if num > 0 else "🔴"
    except:
        return ""
st.title("📈 NSE India Stock Dashboard")
st.markdown("---")
with st.sidebar:
    st.header("⚙️ Controls")
    auto_refresh = st.toggle("Auto-refresh", value=True)
    refresh_interval = st.slider("Refresh interval (seconds)", 30, 300, 60)
    
    if st.button("🔄 Refresh Now", type="primary"):
        refresh_data()
    
    st.markdown("---")
    st.markdown("**Last Updated:**")
    if st.session_state.last_refresh:
        st.write(st.session_state.last_refresh.strftime("%H:%M:%S"))
    else:
        st.write("Never")
    
    elapsed = 0
    if st.session_state.last_refresh:
        elapsed = (datetime.now() - st.session_state.last_refresh).seconds
    remaining = max(0, refresh_interval - elapsed)
    
    if auto_refresh and remaining <= 0:
        refresh_data()
    
    st.markdown(f"**Next refresh in:** {remaining}s")
if st.session_state.data is None:
    refresh_data()
tab1, tab2, tab3 = st.tabs(["📊 Live Indices", "📈 OI Spurts", "🏆 Top Gainers/Losers"])
with tab1:
    st.subheader("Live Market Indices")
    if st.session_state.data and st.session_state.data.get('indices'):
        df = pd.DataFrame(st.session_state.data['indices'])
        cols = st.columns(3)
        for idx, row in df.iterrows():
            if idx < len(cols):
                change = row.get('Change %', 0)
                with cols[idx % 3]:
                    st.metric(label=row.get('Symbol', 'N/A'), value=f"{row.get('Value', 0):,.2f}", delta=f"{change:+.2f}%" if change else None)
        
        st.markdown("### All Indices")
        df_display = df.copy()
        df_display['Status'] = df_display['Change %'].apply(color_change)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("No indices data available.")
with tab2:
    st.subheader("Open Interest Spurts")
    if st.session_state.data and st.session_state.data.get('oi_spurts'):
        df = pd.DataFrame(st.session_state.data['oi_spurts'])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No OI data available.")
with tab3:
    st.subheader("Top Gainers & Losers")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🟢 Top Gainers")
        if st.session_state.data and st.session_state.data.get('gainers'):
            df_gainers = pd.DataFrame(st.session_state.data['gainers'])
            st.dataframe(df_gainers.head(20), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("### 🔴 Top Losers")
        if st.session_state.data and st.session_state.data.get('losers'):
            df_losers = pd.DataFrame(st.session_state.data['losers'])
            st.dataframe(df_losers.head(20), use_container_width=True, hide_index=True)
if auto_refresh:
    time.sleep(1)
    st.rerun()
