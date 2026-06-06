import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from ui.dashboard import render_dashboard
from ui.components import render_sidebar
from database.db_manager import DatabaseManager
from data_fetchers.update_manager import UpdateManager

# Page config
st.set_page_config(
    page_title="Bond Yield Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_db():
    return DatabaseManager()

# Initialize update manager
@st.cache_resource
def init_update_manager():
    return UpdateManager()

def main():
    # Initialize components
    db = init_db()
    update_manager = init_update_manager()
    
    # Sidebar
    country, manual_update = render_sidebar()
    
    # Check for manual update trigger
    if manual_update:
        with st.spinner("กำลังอัปเดตข้อมูล... (อาจใช้เวลา 1-2 นาที)"):
            for c in ['us', 'thailand']:
                update_manager.update_country_data(c)
            st.success("อัปเดตข้อมูลเรียบร้อย!")
            st.rerun()
    
    # Render main dashboard
    render_dashboard(country, db)
    
    # Footer
    st.markdown("---")
    st.caption(f"🕐 Last refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("📊 Data sources: FRED (US) | Investing.com + CPI (Thailand)")

if __name__ == "__main__":
    main()
