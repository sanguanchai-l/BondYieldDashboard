from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for country agents"""
    
    def __init__(self, country_name: str):
        self.country_name = country_name
        self.data = None
    
    @abstractmethod
    def fetch_data(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from source"""
        pass
    
    @abstractmethod
    def process_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Process and clean data"""
        pass
    
    def get_summary_stats(self, data: pd.DataFrame) -> dict:
        """Get summary statistics for the data"""
        if data.empty:
            return {}
        
        stats = {
            'start_date': data['date'].min(),
            'end_date': data['date'].max(),
            'records': len(data),
        }
        
        if 'nominal_yield' in data.columns:
            stats['nominal_mean'] = data['nominal_yield'].mean()
            stats['nominal_min'] = data['nominal_yield'].min()
            stats['nominal_max'] = data['nominal_yield'].max()
            stats['nominal_current'] = data['nominal_yield'].iloc[-1]
        
        if 'real_yield' in data.columns and data['real_yield'].notna().any():
            stats['real_mean'] = data['real_yield'].mean()
            stats['real_current'] = data['real_yield'].iloc[-1]
        
        if 'difference' in data.columns:
            stats['spread_current'] = data['difference'].iloc[-1]
        
        return stats
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data structure"""
        required_columns = ['date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Missing required column: {col}")
                return False
        
        if df.empty:
            logger.warning(f"Empty dataframe for {self.country_name}")
            return False
        
        return True
