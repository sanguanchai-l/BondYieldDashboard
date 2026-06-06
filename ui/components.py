import streamlit as st
import pandas as pd
from datetime import datetime

def render_sidebar():
    """แสดง Sidebar สำหรับเลือกประเทศและปุ่มอัปเดต"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/trending-up.png", width=60)
        st.title("📊 Bond Yield")
        st.markdown("---")
        
        # Country selection
        country = st.radio(
            "เลือกประเทศ",
            ["Thailand", "United States"],
            horizontal=True,
            help="เลือกประเทศที่ต้องการดูข้อมูล"
        )
        
        st.markdown("---")
        
        # Update button
        st.subheader("🔄 Data Management")
        manual_update = st.button(
            "📥 Update Data Now",
            type="primary",
            use_container_width=True,
            help="คลิกเพื่อดึงข้อมูลล่าสุดจากแหล่งข้อมูล"
        )
        
        st.markdown("---")
        
        # Information
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Data Sources:**
            - 🇺🇸 US: FRED (DGS10, DFII10)
            - 🇹🇭 Thailand: Investing.com + CPI
            
            **Real Yield:**
            - US: Direct TIPS data
            - Thailand: Estimated from CPI
            
            **Update Frequency:**
            - Manual update available
            - Auto-check for new data
            """)
        
        # Status indicator
        st.markdown("---")
        st.caption(f"🕐 Session started: {datetime.now().strftime('%H:%M:%S')}")
    
    return country, manual_update

def render_data_table(df: pd.DataFrame, title: str = "Historical Data"):
    """แสดงตารางข้อมูลแบบ sortable"""
    if df.empty:
        st.warning("No data available. Please click 'Update Data' to fetch information.")
        return
    
    # Format for display
    display_df = df.copy()
    display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d')
    
    # Rename columns for better display
    column_mapping = {
        'date': 'Date',
        'nominal_yield': 'Nominal (%)',
        'real_yield': 'Real (%)',
        'difference': 'Spread (bps)'
    }
    display_df = display_df.rename(columns=column_mapping)
    
    # Keep only relevant columns
    cols_to_show = [col for col in column_mapping.values() if col in display_df.columns]
    display_df = display_df[cols_to_show]
    
    # Add data quality indicators
    st.subheader(title)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        if 'nominal_yield' in df.columns:
            latest = df['nominal_yield'].iloc[-1]
            st.metric("Latest Nominal", f"{latest:.2f}%")
    with col3:
        if 'real_yield' in df.columns and df['real_yield'].notna().any():
            latest_real = df['real_yield'].iloc[-1]
            st.metric("Latest Real", f"{latest_real:.2f}%")
    with col4:
        if 'difference' in df.columns:
            latest_spread = df['difference'].iloc[-1]
            st.metric("Latest Spread", f"{latest_spread:.0f} bps")
    
    # Data table with pagination
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "Nominal (%)": st.column_config.NumberColumn("Nominal (%)", format="%.2f"),
            "Real (%)": st.column_config.NumberColumn("Real (%)", format="%.2f"),
            "Spread (bps)": st.column_config.NumberColumn("Spread (bps)", format="%.0f")
        }
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"bond_yields_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def render_metrics_cards(df: pd.DataFrame):
    """แสดง metric cards สำหรับภาพรวม"""
    if df.empty:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'nominal_yield' in df.columns:
            avg_nominal = df['nominal_yield'].mean()
            st.metric("Avg Nominal Yield", f"{avg_nominal:.2f}%")
    
    with col2:
        if 'real_yield' in df.columns and df['real_yield'].notna().any():
            avg_real = df['real_yield'].mean()
            st.metric("Avg Real Yield", f"{avg_real:.2f}%")
        else:
            st.metric("Avg Real Yield", "N/A")
    
    with col3:
        if 'difference' in df.columns:
            avg_spread = df['difference'].mean()
            st.metric("Avg Spread", f"{avg_spread:.0f} bps")
