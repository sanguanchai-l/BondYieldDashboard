import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = os.getenv("DATABASE_PATH", DATA_DIR / "bond_yields.db")

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# FRED API
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
if not FRED_API_KEY:
    print("⚠️ Warning: FRED_API_KEY not set. US data will not work.")

# Thailand data settings
THAILAND_INVESTING_URL = "https://www.investing.com/rates-bonds/thailand-10-year-bond-yield-historical-data"
THAILAND_CPI_FALLBACK = True  # Use CPI for real yield estimation

# Update settings
UPDATE_BATCH_SIZE = 365  # Days per batch
REQUEST_TIMEOUT = 30  # seconds
RETRY_COUNT = 3

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
