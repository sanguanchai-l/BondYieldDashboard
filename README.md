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
echo "FRED_API_KEY=your_api_key_here" > .env

# 5. Run dashboard
streamlit run app.py
