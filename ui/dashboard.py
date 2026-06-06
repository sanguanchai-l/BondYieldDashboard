import streamlit as st
import pandas as pd
from database.db_manager import DatabaseManager
from ui.charts import create_yield_chart
from ui.components import render_data_table, render_metrics_cards

def render_dashboard(country: str, db: DatabaseManager):
    """แสดง Dashboard หลัก"""
    
    # Map country name to database key
    country_key = 'us' if country == "United States" else 'thailand'
    
    # Fetch data from database
    df = db.get_data(country_key)
    
    # Header
    if country == "United States":
        st.header("🇺🇸 United States 10-Year Treasury Yield")
        st.caption("Data source: FRED (DGS10 for Nominal, DFII10 for TIPS)")
    else:
        st.header("🇹🇭 Thailand Government Bond Yield")
        st.caption("Data source: Investing.com (Nominal) | Real yield estimated from CPI")
    
    st.markdown("---")
    
    # Tabs for Data and Graph
    tab1, tab2 = st.tabs(["📈 Graph", "📋 Data Table"])
    
    with tab1:
        if not df.empty:
            # Metrics cards above chart
            render_metrics_cards(df)
            
            # Create and display chart
            title = f"{country} - 10-Year Bond Yields"
            fig = create_yield_chart(df, title)
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional info
            st.caption("💡 Tips: Hover over the chart to see values. Use range selector below to zoom.")
        else:
            st.info("No data available. Please click 'Update Data' in the sidebar to fetch historical data.")
    
    with tab2:
        render_data_table(df, f"{country} - Historical Data")
    
    # Show last update info
    if not df.empty:
        last_date = df['date'].max()
        if isinstance(last_date, pd.Timestamp):
            last_date = last_date.strftime('%Y-%m-%d')
        st.caption(f"📅 Data up to: {last_date}")
