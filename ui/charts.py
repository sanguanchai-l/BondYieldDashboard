import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

def create_yield_chart(df: pd.DataFrame, title: str = "Bond Yields") -> go.Figure:
    """
    สร้างกราฟเส้น 3 เส้น (Nominal, Real, Difference)
    พร้อม hover tooltip แสดงค่าเมื่อเลื่อนเมาส์
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Create figure with secondary y-axis for spread
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add Nominal Yield line
    if 'nominal_yield' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['nominal_yield'],
                mode='lines+markers',
                name='Nominal Yield',
                line=dict(color='#2E86AB', width=2),
                marker=dict(size=4, color='#2E86AB'),
                hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                              'Nominal: %{y:.2f}%<extra></extra>'
            ),
            secondary_y=False
        )
    
    # Add Real Yield line
    if 'real_yield' in df.columns and df['real_yield'].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['real_yield'],
                mode='lines+markers',
                name='Real Yield',
                line=dict(color='#A23B72', width=2, dash='dot'),
                marker=dict(size=4, color='#A23B72'),
                hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                              'Real: %{y:.2f}%<extra></extra>'
            ),
            secondary_y=False
        )
    
    # Add Spread (Difference) as bar chart on secondary axis
    if 'difference' in df.columns and df['difference'].notna().any():
        fig.add_trace(
            go.Bar(
                x=df['date'],
                y=df['difference'],
                name='Spread (bps)',
                marker=dict(color='#F18F01', opacity=0.3),
                hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                              'Spread: %{y:.0f} bps<extra></extra>'
            ),
            secondary_y=True
        )
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, x=0.5),
        xaxis=dict(
            title="Date",
            tickformat="%Y",
            rangeslider=dict(visible=True, thickness=0.05),
            type="date"
        ),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        margin=dict(l=60, r=60, t=80, b=60)
    )
    
    # Update y-axes labels
    fig.update_yaxes(title_text="Yield (%)", secondary_y=False)
    fig.update_yaxes(title_text="Spread (basis points)", secondary_y=True)
    
    # Add range selector buttons
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=3, label="3Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(count=10, label="10Y", step="year", stepmode="backward"),
                dict(label="All", step="all")
            ]),
            x=0.8, y=1.1
        )
    )
    
    return fig

def create_comparison_chart(us_df: pd.DataFrame, th_df: pd.DataFrame) -> go.Figure:
    """สร้างกราฟเปรียบเทียบระหว่างสองประเทศ (เฉพาะ Nominal)"""
    fig = go.Figure()
    
    if not us_df.empty and 'nominal_yield' in us_df.columns:
        fig.add_trace(
            go.Scatter(
                x=us_df['date'],
                y=us_df['nominal_yield'],
                mode='lines',
                name='US 10Y',
                line=dict(color='#2E86AB', width=2)
            )
        )
    
    if not th_df.empty and 'nominal_yield' in th_df.columns:
        fig.add_trace(
            go.Scatter(
                x=th_df['date'],
                y=th_df['nominal_yield'],
                mode='lines',
                name='Thailand 10Y',
                line=dict(color='#A23B72', width=2)
            )
        )
    
    fig.update_layout(
        title="Nominal Yield Comparison: US vs Thailand",
        xaxis_title="Date",
        yaxis_title="Yield (%)",
        hovermode='x unified',
        height=450
    )
    
    return fig
