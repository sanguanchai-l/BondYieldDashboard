import unittest
import os
import tempfile
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    
    def setUp(self):
        """สร้าง temp database สำหรับทดสอบ"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.db = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """ลบ temp database หลังทดสอบ"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
    
    def test_init_database(self):
        """ทดสอบการสร้างฐานข้อมูล"""
        self.assertTrue(os.path.exists(self.db_path))
    
    def test_insert_and_get_data(self):
        """ทดสอบการบันทึกและดึงข้อมูล"""
        # สร้าง test data
        test_df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'nominal_yield': [3.5, 3.6],
            'real_yield': [1.2, 1.3],
            'difference': [230, 230],
            'data_source': ['test', 'test']
        })
        test_df['date'] = pd.to_datetime(test_df['date'])
        
        # บันทึกข้อมูล
        rows = self.db.insert_yield_data('us', test_df)
        self.assertEqual(rows, 2)
        
        # ดึงข้อมูล
        df = self.db.get_data('us')
        self.assertEqual(len(df), 2)
        self.assertIn('nominal_yield', df.columns)
    
    def test_get_last_update_date(self):
        """ทดสอบการดึงวันที่ล่าสุด"""
        # เริ่มต้นควรเป็น None
        last_date = self.db.get_last_update_date('us')
        self.assertIsNone(last_date)
        
        # เพิ่มข้อมูล
        test_df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'nominal_yield': [3.5, 3.6],
            'data_source': ['test', 'test']
        })
        test_df['date'] = pd.to_datetime(test_df['date'])
        self.db.insert_yield_data('us', test_df)
        
        # ตรวจสอบวันที่ล่าสุด
        last_date = self.db.get_last_update_date('us')
        self.assertEqual(str(last_date), '2024-01-02')
    
    def test_get_record_count(self):
        """ทดสอบการนับจำนวนเรคคอร์ด"""
        count = self.db.get_record_count('us')
        self.assertEqual(count, 0)
        
        test_df = pd.DataFrame({
            'date': ['2024-01-01'],
            'nominal_yield': [3.5],
            'data_source': ['test']
        })
        test_df['date'] = pd.to_datetime(test_df['date'])
        self.db.insert_yield_data('us', test_df)
        
        count = self.db.get_record_count('us')
        self.assertEqual(count, 1)
    
    def test_log_update(self):
        """ทดสอบการบันทึกประวัติการอัปเดต"""
        self.db.log_update('us', 'success', 'Test update', '2024-01-01', 100)
        
        with self.db.get_connection() as conn:
            result = conn.execute(
                "SELECT * FROM update_log WHERE country = ?", ('us',)
            ).fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[4], 100)  # record_count

if __name__ == '__main__':
    unittest.main()
