# NSE Stock Market Dashboard - Specification

## Project Overview
- **Project Name**: NSE India Stock Dashboard
- **Type**: Interactive data dashboard
- **Core Functionality**: Scrape and display live market data from NSE India (indices, OI spurs, top gainers/losers) with auto-refresh
- **Target Users**: Indian stock market traders and analysts

## Data Sources
1. **Live Market Indices**: https://www.nseindia.com/market-data/live-market-indices
2. **OI Spurts**: https://www.nseindia.com/market-data/oi-spurts
3. **Top Gainers/Losers**: https://www.nseindia.com/market-data/top-gainers-losers

## UI/UX Specification

### Layout
- Single page with 3 tabs for each data source
- Sidebar with controls (refresh interval, export options)
- Clean, professional dark theme

### Visual Design
- **Color Palette**:
  - Background: #0e1117 (dark)
  - Card Background: #1e293b
  - Primary: #22c55e (green for gains)
  - Secondary: #ef4444 (red for losses)
  - Accent: #3b82f6 (blue)
  - Text: #e2e8f0
- **Typography**: System font, clear data tables
- **Spacing**: 16px padding, 8px gaps

### Components
- Tab navigation for 3 views
- Data tables with sorting
- Auto-refresh indicator with countdown timer
- Last updated timestamp

## Functionality Specification

### Core Features
1. **Data Scraping**: Extract data from NSE India using Selenium (NSE uses dynamic JS)
2. **Auto-refresh**: Refresh data every 60 seconds (configurable)
3. **Live Indices Tab**: Display all major indices (Nifty 50, Bank Nifty, etc.) with values and change %
4. **OI Spurts Tab**: Show Open Interest analysis with % change
5. **Top Gainers/Losers Tab**: Display top gainers and losers with price, change %

### User Interactions
- Switch between tabs
- Manual refresh button
- Auto-refresh toggle

### Data Handling
- Cache data to avoid excessive requests
- Graceful error handling for failed requests

## Acceptance Criteria
- [ ] Dashboard loads without errors
- [ ] All 3 NSE pages are scraped successfully
- [ ] Auto-refresh works every 60 seconds
- [ ] Data displays in tabular format
- [ ] Green/red coloring for positive/negative changes
