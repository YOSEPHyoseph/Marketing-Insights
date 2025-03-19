import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Load and prepare the data
@st.cache_data
def load_data():
    file_path = r'C:\Users\Yoseph\Desktop\New folder\campaign_data.xlsx'  # Update to your Excel file name
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None
    
    data['Date'] = pd.to_datetime(data['Date'])
    # Add day of week for heatmap
    data['Day of Week'] = data['Date'].dt.day_name()
    return data

# Calculate key metrics
def calculate_metrics(df):
    total_spend = df['Spend, GBP'].sum()
    total_impressions = df['Impressions'].sum()
    total_clicks = df['Clicks'].sum()
    total_conversions = df['Conversions'].sum()
    total_conversion_value = df['Total conversion value, GBP'].sum()
    avg_ctr = df['CTR, %'].mean() * 100  # Convert to percentage
    avg_cpc = df['Daily Average CPC'].mean()
    roas = total_conversion_value / total_spend if total_spend > 0 else 0
    cost_per_conversion = total_spend / total_conversions if total_conversions > 0 else 0
    conversion_rate = (total_conversions / total_clicks) * 100 if total_clicks > 0 else 0
    
    return {
        'Total Spend (£)': total_spend,
        'Impressions': total_impressions,
        'Clicks': total_clicks,
        'Conversions': total_conversions,
        'Conversion Value (£)': total_conversion_value,
        'Avg CTR (%)': avg_ctr,
        'Avg CPC (£)': avg_cpc,
        'ROAS': roas,
        'Cost Per Conversion (£)': cost_per_conversion,
        'Conversion Rate (%)': conversion_rate
    }

# Main dashboard
def main():
    st.set_page_config(layout="wide")
    st.title("Advertising Campaign Dashboard")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    campaigns = st.sidebar.multiselect("Campaign", options=df['Campaign'].unique(), default=df['Campaign'].unique())
    channels = st.sidebar.multiselect("Channel", options=df['Channel'].unique(), default=df['Channel'].unique())
    cities = st.sidebar.multiselect("City", options=df['City/Location'].unique(), default=df['City/Location'].unique())
    devices = st.sidebar.multiselect("Device", options=df['Device'].unique(), default=df['Device'].unique())
    date_range = st.sidebar.date_input("Date Range", 
                                     [df['Date'].min(), df['Date'].max()],
                                     min_value=df['Date'].min(),
                                     max_value=df['Date'].max())
    
    # Filter data
    filtered_df = df[
        (df['Campaign'].isin(campaigns)) &
        (df['Channel'].isin(channels)) &
        (df['City/Location'].isin(cities)) &
        (df['Device'].isin(devices)) &
        (df['Date'].dt.date >= date_range[0]) &
        (df['Date'].dt.date <= date_range[1])
    ]
    
    # Key Metrics
    metrics = calculate_metrics(filtered_df)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Spend", f"£{metrics['Total Spend (£)']:,.2f}")
        st.metric("Impressions", f"{metrics['Impressions']:,.0f}")
    with col2:
        st.metric("Clicks", f"{metrics['Clicks']:,.0f}")
        st.metric("Conversions", f"{metrics['Conversions']:,.0f}")
    with col3:
        st.metric("Conversion Value", f"£{metrics['Conversion Value (£)']:,.2f}")
        st.metric("Avg CTR", f"{metrics['Avg CTR (%)']:.2f}%")
    with col4:
        st.metric("Avg CPC", f"£{metrics['Avg CPC (£)']:.2f}")
        st.metric("ROAS", f"{metrics['ROAS']:.2f}x")
    with col5:
        st.metric("Cost/Conv", f"£{metrics['Cost Per Conversion (£)']:.2f}")
        st.metric("CVR", f"{metrics['Conversion Rate (%)']:.2f}%")
    
    # Performance Trends
    st.header("Performance Trends")
    tab1, tab2, tab3 = st.tabs(["Spend vs Conversion Value", "Impressions vs Clicks", "CTR Over Time"])
    
    with tab1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=filtered_df.groupby('Date')['Spend, GBP'].sum().index,
                                 y=filtered_df.groupby('Date')['Spend, GBP'].sum(),
                                 name='Spend (£)', line=dict(color='blue')))
        fig1.add_trace(go.Scatter(x=filtered_df.groupby('Date')['Total conversion value, GBP'].sum().index,
                                 y=filtered_df.groupby('Date')['Total conversion value, GBP'].sum(),
                                 name='Conversion Value (£)', line=dict(color='green'), yaxis='y2'))
        fig1.update_layout(yaxis2=dict(overlaying='y', side='right'), title="Spend vs Conversion Value Over Time")
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        fig2 = px.line(filtered_df.groupby('Date').agg({'Impressions': 'sum', 'Clicks': 'sum'}).reset_index(),
                      x='Date', y=['Impressions', 'Clicks'], title="Impressions vs Clicks Over Time")
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        fig3 = px.line(filtered_df.groupby('Date')['CTR, %'].mean().reset_index(),
                      x='Date', y='CTR, %', title="Average CTR Over Time")
        st.plotly_chart(fig3, use_container_width=True)
    
    # New Insights Section
    st.header("Additional Insights")
    
    # Daily Performance Heatmap
    st.subheader("Daily Performance by Day of Week")
    heatmap_data = filtered_df.groupby('Day of Week').agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Conversions': 'sum'
    }).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    fig6 = px.imshow(heatmap_data.T, labels=dict(x="Day of Week", y="Metric", color="Value"),
                    title="Performance Heatmap by Day of Week")
    st.plotly_chart(fig6, use_container_width=True)
    
    # Device Performance
    st.subheader("Device Performance Comparison")
    device_df = filtered_df.groupby('Device').agg({
        'Spend, GBP': 'sum',
        'Conversions': 'sum',
        'Total conversion value, GBP': 'sum',
        'Clicks': 'sum'
    }).reset_index()
    fig7 = px.bar(device_df, x='Device', y=['Spend, GBP', 'Total conversion value, GBP', 'Clicks'],
                 barmode='group', title="Device Performance Metrics")
    st.plotly_chart(fig7, use_container_width=True)
    
    # Top Performing Ads
    st.subheader("Top Performing Ads (by Conversion Value)")
    top_ads = filtered_df.groupby(['Campaign', 'Ad', 'Channel']).agg({
        'Total conversion value, GBP': 'sum',
        'Spend, GBP': 'sum',
        'Conversions': 'sum'
    }).reset_index()
    top_ads['ROAS'] = top_ads['Total conversion value, GBP'] / top_ads['Spend, GBP']
    top_ads = top_ads.sort_values('Total conversion value, GBP', ascending=False).head(5)
    st.dataframe(top_ads.style.format({
        'Total conversion value, GBP': '£{:,.2f}',
        'Spend, GBP': '£{:,.2f}',
        'ROAS': '{:.2f}x'
    }))
    
    # Geographical Visualization
    st.subheader("Geographical Performance")
    geo_df = filtered_df.groupby(['City/Location', 'Latitude', 'Longitude']).agg({
        'Total conversion value, GBP': 'sum',
        'Spend, GBP': 'sum',
        'Conversions': 'sum'
    }).reset_index()
    fig8 = px.scatter_geo(geo_df, lat='Latitude', lon='Longitude', size='Total conversion value, GBP',
                         color='Conversions', hover_name='City/Location',
                         title="Geographical Performance (Size = Conversion Value, Color = Conversions)")
    fig8.update_layout(geo=dict(scope='europe', showland=True))
    st.plotly_chart(fig8, use_container_width=True)
    
    # Channel Performance
    st.header("Channel Performance")
    channel_df = filtered_df.groupby('Channel').agg({
        'Spend, GBP': 'sum',
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Conversions': 'sum',
        'Total conversion value, GBP': 'sum'
    }).reset_index()
    fig4 = px.bar(channel_df, x='Channel', y=['Spend, GBP', 'Total conversion value, GBP'],
                 barmode='group', title="Spend vs Conversion Value by Channel")
    st.plotly_chart(fig4, use_container_width=True)
    
    # Campaign Performance
    st.header("Campaign Performance")
    campaign_df = filtered_df.groupby('Campaign').agg({
        'Spend, GBP': 'sum',
        'Conversions': 'sum',
        'Total conversion value, GBP': 'sum'
    }).reset_index()
    fig5 = px.scatter(campaign_df, x='Spend, GBP', y='Total conversion value, GBP', size='Conversions',
                     color='Campaign', title="Campaign Performance (Size = Conversions)")
    st.plotly_chart(fig5, use_container_width=True)
    
    # Raw Data
    st.header("Raw Data")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()