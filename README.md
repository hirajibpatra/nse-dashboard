# NSE India Stock Dashboard

Interactive dashboard for Indian stock market analysis with live data from NSE India.

## Features

- **Live Market Indices**: Real-time data for Nifty 50, Bank Nifty, Sensex, and sectoral indices
- **OI Spurts**: Open Interest analysis showing stocks with significant OI changes
- **Top Gainers/Losers**: Most gainers and losers in the market
- **Auto-refresh**: Configurable auto-refresh (default 60 seconds)

## Setup

```bash
cd nse-dashboard
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## Data Sources

1. Live Market Indices: https://www.nseindia.com/market-data/live-market-indices
2. OI Spurts: https://www.nseindia.com/market-data/oi-spurts
3. Top Gainers/Losers: https://www.nseindia.com/market-data/top-gainers-losers

Note: Indices data is fetched via Yahoo Finance. OI and gainers/losers use sample data (NSE website requires more complex setup for live scraping).
