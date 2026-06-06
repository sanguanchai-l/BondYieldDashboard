import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "data/bond_yields.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with schema if not exists"""
        # Ensure data directory exists
        Path(self.db_path).parent.mkdir(exist_ok=True)
        
        # Read schema
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, "r") as f:
                schema = f.read()
            
            with self.get_connection() as conn:
                conn.executescript(schema)
                logger.info(f"Database initialized at {self.db_path}")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def insert_yield_data(self, country: str, df: pd.DataFrame) -> int:
        """
        Insert or replace yield data
        Returns: Number of rows inserted
        """
        if df.empty:
            return 0
        
        rows_affected = 0
        with self.get_connection() as conn:
            for _, row in df.iterrows():
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO bond_yields 
                        (country, date, nominal_yield, real_yield, difference, data_source)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        country,
                        row['date'],
                        row.get('nominal_yield'),
                        row.get('real_yield'),
                        row.get('difference'),
                        row.get('data_source', 'unknown')
                    ))
                    rows_affected += 1
                except Exception as e:
                    logger.error(f"Error inserting row {row.get('date')}: {e}")
        
        logger.info(f"Inserted {rows_affected} rows for {country}")
        return rows_affected
    
    def get_data(self, country: str, start_date: Optional[str] = None, 
                 end_date: Optional[str] = None) -> pd.DataFrame:
        """Get yield data for a country"""
        query = """
            SELECT date, nominal_yield, real_yield, difference 
            FROM bond_yields 
            WHERE country = ?
        """
        params = [country]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date"
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=params)
        
        # Convert date to datetime
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
        
        return df
    
    def get_last_update_date(self, country: str) -> Optional[str]:
        """Get latest date in database for a country"""
        with self.get_connection() as conn:
            result = conn.execute("""
                SELECT MAX(date) FROM bond_yields WHERE country = ?
            """, (country,)).fetchone()
        
        return result[0] if result[0] else None
    
    def get_record_count(self, country: str) -> int:
        """Get total record count for a country"""
        with self.get_connection() as conn:
            result = conn.execute("""
                SELECT COUNT(*) FROM bond_yields WHERE country = ?
            """, (country,)).fetchone()
        
        return result[0] if result[0] else 0
    
    def log_update(self, country: str, status: str, message: str = "", 
                   last_update: Optional[str] = None, record_count: int = 0):
        """Log an update attempt"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO update_log (country, last_update, last_fetch, 
                                        record_count, status, message)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                country, last_update, datetime.now(), 
                record_count, status, message
            ))
    
    def close(self):
        """Close database connection (no-op for sqlite3)"""
        pass