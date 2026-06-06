import pandas as pd
from typing import Optional
from datetime import datetime, timedelta
import logging

from .base_agent import BaseAgent
from data_fetchers.fred_fetcher import FREDFetcher

logger = logging.getLogger(__name__)

class USAgent(BaseAgent):
    """Agent for United States bond yield data"""
    
    def __init__(self):
        super().__init__("United States")
        self.fetcher = FREDFetcher()
    
    def fetch_data(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch US data from FRED"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')
        
        logger.info(f"Fetching US data from {start_date} to {end_date or 'present'}")
        df = self.fetcher.fetch_all_us_data(start_date, end_date)
        
        if self.validate_data(df):
            self.data = self.process_data(df)
            return self.data
        else:
            logger.error("US data validation failed")
            return pd.DataFrame()
    
    def process_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Process US data"""
        df = raw_data.copy()
        
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Fill missing values (forward fill for holidays/weekends)
        df = df.set_index('date').asfreq('D').fillna(method='ffill').reset_index()
        
        # Round yields to 2 decimal places
        if 'nominal_yield' in df.columns:
            df['nominal_yield'] = df['nominal_yield'].round(2)
        if 'real_yield' in df.columns:
            df['real_yield'] = df['real_yield'].round(2)
        if 'difference' in df.columns:
            df['difference'] = df['difference'].round(0)
        
        logger.info(f"Processed {len(df)} US records")
        return df
    
    def get_tips_info(self) -> dict:
        """Get information about TIPS data"""
        return {
            'description': '10-Year Treasury Inflation-Protected Securities (TIPS)',
            'fred_series': 'DFII10',
            'notes': 'Constant maturity yield, inflation-adjusted'
        }
