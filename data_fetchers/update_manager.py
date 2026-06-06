import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging

from database.db_manager import DatabaseManager
from agents.us_agent import USAgent
from agents.thailand_agent import ThailandAgent

logger = logging.getLogger(__name__)

class UpdateManager:
    """จัดการการอัปเดตข้อมูลจากแหล่งต่างๆ"""
    
    def __init__(self, db_path: str = "data/bond_yields.db"):
        self.db = DatabaseManager(db_path)
        self.us_agent = USAgent()
        self.thai_agent = ThailandAgent()
    
    def check_last_update(self, country: str) -> Tuple[Optional[str], int]:
        """
        ตรวจสอบข้อมูลล่าสุดในฐานข้อมูล
        Returns: (last_date, record_count)
        """
        last_date = self.db.get_last_update_date(country)
        record_count = self.db.get_record_count(country)
        return last_date, record_count
    
    def needs_update(self, country: str, max_age_days: int = 7) -> bool:
        """
        ตรวจสอบว่าต้องอัปเดตข้อมูลหรือไม่
        อัปเดตถ้า:
        1. ไม่มีข้อมูลเลย
        2. ข้อมูลล่าสุดเก่ากว่า max_age_days วัน
        """
        last_date, _ = self.check_last_update(country)
        
        if last_date is None:
            logger.info(f"No data for {country}, update needed")
            return True
        
        # Convert to date if string
        if isinstance(last_date, str):
            last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
        elif hasattr(last_date, 'date'):
            last_date = last_date.date()
        
        days_since = (datetime.now().date() - last_date).days
        needs_update = days_since > max_age_days
        
        if needs_update:
            logger.info(f"{country} last updated {days_since} days ago, update needed")
        else:
            logger.info(f"{country} data is fresh ({days_since} days old)")
        
        return needs_update
    
    def update_country_data(self, country: str, force: bool = False) -> dict:
        """
        อัปเดตข้อมูลของประเทศใดประเทศหนึ่ง
        Returns: dict with status and details
        """
        result = {
            'country': country,
            'status': 'success',
            'records_added': 0,
            'message': ''
        }
        
        try:
            # Check if update is needed
            if not force and not self.needs_update(country):
                result['message'] = f"{country} data is up to date"
                self.db.log_update(country, 'skipped', result['message'])
                return result
            
            # Fetch new data
            if country == 'us':
                agent = self.us_agent
            elif country == 'thailand':
                agent = self.thai_agent
            else:
                raise ValueError(f"Unknown country: {country}")
            
            # Get last date to fetch from
            last_date, _ = self.check_last_update(country)
            if last_date and not force:
                # Fetch from day after last date
                start_date = (datetime.strptime(str(last_date), '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                start_date = None  # Fetch all 10 years
            
            # Fetch data
            new_data = agent.fetch_data(start_date)
            
            if new_data.empty:
                result['status'] = 'warning'
                result['message'] = f"No new data available for {country}"
            else:
                # Insert into database
                rows = self.db.insert_yield_data(country, new_data)
                result['records_added'] = rows
                result['message'] = f"Added {rows} new records"
            
            # Log the update
            new_last_date = self.db.get_last_update_date(country)
            new_count = self.db.get_record_count(country)
            self.db.log_update(
                country, 
                result['status'], 
                result['message'],
                str(new_last_date) if new_last_date else None,
                new_count
            )
            
        except Exception as e:
            result['status'] = 'failed'
            result['message'] = str(e)
            logger.error(f"Update failed for {country}: {e}")
            self.db.log_update(country, 'failed', str(e))
        
        return result
    
    def update_all_countries(self, force: bool = False) -> dict:
        """อัปเดตข้อมูลทุกประเทศ"""
        results = {}
        
        for country in ['us', 'thailand']:
            results[country] = self.update_country_data(country, force)
        
        return results
    
    def get_update_status(self) -> pd.DataFrame:
        """แสดงสถานะการอัปเดตล่าสุดของทุกประเทศ"""
        with self.db.get_connection() as conn:
            query = """
                SELECT country, last_update, last_fetch, record_count, status, message
                FROM update_log
                WHERE (country, created_at) IN (
                    SELECT country, MAX(created_at)
                    FROM update_log
                    GROUP BY country
                )
                ORDER BY country
            """
            df = pd.read_sql_query(query, conn)    
        return df

