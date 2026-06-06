import pandas as pd
from typing import Optional
from datetime import datetime, timedelta
import logging

from .base_agent import BaseAgent
from data_fetchers.thai_fetcher import ThaiFetcher

logger = logging.getLogger(__name__)

class ThailandAgent(BaseAgent):
    """Agent for Thailand bond yield data"""
    
    def __init__(self):
        super().__init__("Thailand")
        self.fetcher = ThaiFetcher()
    
    def fetch_data(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch Thailand data"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')
        
        logger.info(f"Fetching Thailand data from {start_date} to {end_date or 'present'}")
        df = self.fetcher.fetch_all_thai_data(start_date, end_date)
        
        if self.validate_data(df):
            self.data = self.process_data(df)
            return self.data
        else:
            logger.error("Thailand data validation failed")
            return pd.DataFrame()
    
    def process_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Process Thailand data"""
        df = raw_data.copy()
        
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Fill missing values (forward fill)
        df = df.set_index('date').asfreq('D').fillna(method='ffill').reset_index()
        
        # Round yields to 2 decimal places
        if 'nominal_yield' in df.columns:
            df['nominal_yield'] = df['nominal_yield'].round(2)
        if 'real_yield' in df.columns:
            df['real_yield'] = df['real_yield'].round(2)
        if 'difference' in df.columns:
            df['difference'] = df['difference'].round(0)
        
        logger.info(f"Processed {len(df)} Thailand records")
        return df
    
    def get_data_note(self) -> str:
        """Note about Thailand real yield calculation"""
        return "Real yield estimated using CPI inflation (monthly data forward-filled)"
