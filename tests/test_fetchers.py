import unittest
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from data_fetchers.fred_fetcher import FREDFetcher
from data_fetchers.thai_fetcher import ThaiFetcher

class TestFREDFetcher(unittest.TestCase):
    
    def setUp(self):
        self.fetcher = FREDFetcher()
    
    def test_fetch_nominal(self):
        """ทดสอบการดึงข้อมูล US nominal yield"""
        # ทดสอบดึงข้อมูลแค่ 30 วัน
        df = self.fetcher.fetch_10yr_nominal(
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        
        # ถ้าไม่มี API key หรือ network error ให้ผ่าน
        if self.fetcher.fred is None:
            self.assertTrue(df.empty)
        else:
            self.assertIn('nominal_yield', df.columns)
            self.assertIn('date', df.columns)
    
    def test_fetch_real(self):
        """ทดสอบการดึงข้อมูล US real yield (TIPS)"""
        df = self.fetcher.fetch_10yr_real_tips(
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        
        if self.fetcher.fred is None:
            self.assertTrue(df.empty)
        else:
            self.assertIn('real_yield', df.columns)

class TestThaiFetcher(unittest.TestCase):
    
    def setUp(self):
        self.fetcher = ThaiFetcher()
    
    def test_fetch_nominal(self):
        """ทดสอบการดึงข้อมูล Thai nominal yield"""
        df = self.fetcher.fetch_10yr_nominal(
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        
        self.assertFalse(df.empty)
        self.assertIn('nominal_yield', df.columns)
        self.assertIn('date', df.columns)
    
    def test_fetch_cpi(self):
        """ทดสอบการดึงข้อมูล CPI"""
        df = self.fetcher.fetch_cpi_data(
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        
        self.assertFalse(df.empty)
        self.assertIn('inflation', df.columns)
    
    def test_fetch_all(self):
        """ทดสอบการดึงข้อมูลทั้งหมด"""
        df = self.fetcher.fetch_all_thai_data(
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        
        self.assertFalse(df.empty)
        self.assertIn('nominal_yield', df.columns)
        self.assertIn('real_yield', df.columns)
        self.assertIn('difference', df.columns)

if __name__ == '__main__':
    unittest.main()
