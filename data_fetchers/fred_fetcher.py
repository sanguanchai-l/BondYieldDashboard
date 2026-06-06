import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class FREDFetcher:
    """Fetch US Treasury yield data from FRED API"""
    
    def __init__(self):
        self.api_key = os.getenv('FRED_API_KEY')
        if not self.api_key:
            logger.warning("FRED_API_KEY not set. US data will not be available.")
            self.fred = None
        else:
            try:
                from fredapi import Fred
                self.fred = Fred(api_key=self.api_key)
            except ImportError:
                logger.error("fredapi not installed. Run: pip install fredapi")
                self.fred = None
    
    def fetch_10yr_nominal(self, start_date: Optional[str] = None, 
                           end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch 10-Year Treasury Constant Maturity Rate (DGS10)
        Returns DataFrame with columns: date, nominal_yield, data_source
        """
        if not self.fred:
            return pd.DataFrame()
        
        try:
            series = self.fred.get_series('DGS10', start_date, end_date)
            df = pd.DataFrame({'date': series.index, 'nominal_yield': series.values})
            df['data_source'] = 'FRED'
            logger.info(f"Fetched {len(df)} records for US 10Y nominal yield")
            return df
        except Exception as e:
            logger.error(f"Error fetching US nominal yield: {e}")
            return pd.DataFrame()
    
    def fetch_10yr_real_tips(self, start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch 10-Year Treasury Inflation-Indexed Security (DFII10) - TIPS
        Returns DataFrame with columns: date, real_yield, data_source
        """
        if not self.fred:
            return pd.DataFrame()
        
        try:
            series = self.fred.get_series('DFII10', start_date, end_date)
            df = pd.DataFrame({'date': series.index, 'real_yield': series.values})
            df['data_source'] = 'FRED'
            logger.info(f"Fetched {len(df)} records for US 10Y real yield (TIPS)")
            return df
        except Exception as e:
            logger.error(f"Error fetching US real yield: {e}")
            return pd.DataFrame()
    
    def fetch_all_us_data(self, start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch both nominal and real yields, merge them
        Returns DataFrame with: date, nominal_yield, real_yield, difference, data_source
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')
        
        nominal_df = self.fetch_10yr_nominal(start_date, end_date)
        real_df = self.fetch_10yr_real_tips(start_date, end_date)
        
        if nominal_df.empty and real_df.empty:
            logger.warning("Both nominal and real US data fetches failed")
            return pd.DataFrame()
        
        # Merge on date
        merged = pd.merge(nominal_df, real_df, on=['date', 'data_source'], how='outer')
        
        # Calculate difference (spread) in basis points
        if 'nominal_yield' in merged.columns and 'real_yield' in merged.columns:
            merged['difference'] = (merged['nominal_yield'] - merged['real_yield']) * 100
        
        merged = merged.sort_values('date')
        
        # Fill missing source
        merged['data_source'] = merged['data_source'].fillna('FRED')
        
        logger.info(f"US data merged: {len(merged)} total records")
        return merged
