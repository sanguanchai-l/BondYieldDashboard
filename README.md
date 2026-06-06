markdown
# Bond Yield Dashboard 📈

Dashboard สำหรับติดตามอัตราผลตอบแทนพันธบัตรรัฐบาลอายุ 10 ปี (10-Year Treasury Yield) ของประเทศไทยและสหรัฐอเมริกา

## Features

- 🇹🇭 **Thailand**: 10-year government bond yield + Real yield (estimated from CPI)
- 🇺🇸 **United States**: 10-year Treasury yield + TIPS (Real yield)
- 📊 **Interactive Charts**: 3 lines (Nominal, Real, Spread) with hover tooltips
- 📋 **Data Table**: Sortable and filterable historical data
- 🔄 **Manual Update**: One-click refresh from data sources
- 💾 **SQLite Database**: 10 years of historical data

## Installation

### Prerequisites
- Python 3.9 or higher
- FRED API key (free) → [Register here](https://fred.stlouisfed.org/docs/api/api_key.html)

### Steps

```bash
# 1. Clone repository
git clone https://github.com/sanguanchai-l/BondYieldDashboard.git
cd BondYieldDashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set FRED API key
cp .env.example .env
# Then edit .env file and add your FRED_API_KEY

# 5. Run dashboard
streamlit run app.py
```

## Usage

- Open browser to http://localhost:8501
- Select country from sidebar (Thailand / United States)
- View Data Table for historical values
- View Graph for yield trends
- Click Update Data to fetch latest information

## Data Sources

| Country | Nominal Yield | Real Yield |
|---------|---------------|------------|
| United States | [FRED (DGS10)](https://fred.stlouisfed.org/series/DGS10) | [FRED TIPS (DFII10)](https://fred.stlouisfed.org/series/DFII10) |
| Thailand | [Investing.com](https://www.investing.com/rates-bonds/thailand-10-year-bond-yield-historical-data) (sample) | CPI-adjusted estimate |

## Project Structure

```text
BondYieldDashboard/
├── app.py                 # Main entry point
├── agents/               # Country-specific agents
├── database/             # SQLite operations
├── data_fetchers/        # API and web scraping
├── ui/                   # Streamlit UI components
├── config/               # Settings
└── tests/                # Unit tests
```

## Docker Deployment

```bash
# Build image
docker build -t bond-dashboard .

# Run container
docker run -p 8501:8501 --env-file .env bond-dashboard

# Or use docker-compose
docker-compose up -d
```

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run specific test file
python tests/test_database.py
python tests/test_fetchers.py
```

## Notes

- Thailand real yield is estimated using CPI (no direct TIPS equivalent)
- First run may take 30-60 seconds to fetch 10 years of data
- FRED API key is required for US data
- Data is stored locally in data/bond_yields.db

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ``` ModuleNotFoundError	``` | Run ``` pip install -r requirements.txt ``` again |
| FRED API key invalid | Check ``` .env ``` file and re-register for free key |
| No Thailand data | System uses fallback sample data |
| Chart not showing | Go to Data Table tab first to verify data exists |

## License

MIT
