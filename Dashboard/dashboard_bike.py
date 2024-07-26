import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import streamlit as st

# Load dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/fahrurojak/Bike-Sharing_Dicoding/main/Dataset/day.csv")

# Removing the windspeed column (not relevant to the business question)
drop_columns = ['instant', 'windspeed']

for col in day_df.columns:
    if col in drop_columns:
        day_df.drop(labels=col, axis=1, inplace=True)

# Changing column names (Optional)
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Changing the data type of the dateday column to datetime.
day_df['dateday'] = pd.to_datetime(day_df['dateday'])

# Changing data types
day_df['weekday'] = day_df['dateday'].dt.day_name()
day_df['year'] = day_df['dateday'].dt.year

# Season column
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

# Weathersit column
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Resampling data based on month and calculating total rides
monthly_rent_df = day_df.resample(rule='M', on='dateday').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
})

# Change index format to month-year (Jan-20, Feb-20, etc.)
monthly_rent_df.index = monthly_rent_df.index.strftime('%b-%y')
monthly_rent_df = monthly_rent_df.reset_index()

# Rename columns
monthly_rent_df.rename(columns={
    "dateday": "yearmonth",
    "count": "total_rides",
    "casual": "casual_rides",
    "registered": "registered_rides"
}, inplace=True)

# Grouping and aggregating data
grouped_by_month = day_df.groupby('month')
aggregated_stats_by_month = grouped_by_month['count'].agg(['max', 'min', 'mean', 'sum'])

grouped_by_weather = day_df.groupby('weathersit')
aggregated_stats_by_weather = grouped_by_weather['count'].agg(['max', 'min', 'mean', 'sum'])

grouped_by_holiday = day_df.groupby('holiday')
aggregated_stats_by_holiday = grouped_by_holiday['count'].agg(['max', 'min', 'mean', 'sum'])

grouped_by_weekday = day_df.groupby('weekday')
aggregated_stats_by_weekday = grouped_by_weekday['count'].agg(['max', 'min', 'mean'])

grouped_by_workingday = day_df.groupby('workingday')
aggregated_stats_by_workingday = grouped_by_workingday['count'].agg(['max', 'min', 'mean'])

grouped_by_season = day_df.groupby('season')
aggregated_stats_by_season = grouped_by_season.agg({
    'casual': 'mean',
    'registered': 'mean',
    'count': ['max', 'min', 'mean']
})

# Additional data aggregations
aggregated_stats_by_season_temp = day_df.groupby('season').agg({
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# CSS styling for minimalistic and user-friendly UI with animation
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    * {
        font-family: 'Roboto', sans-serif;
        transition: all 0.5s ease;
    }
    
    .main {
        background-color: #f8f9fa;
        color: #333333;
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
    }

    .sidebar .sidebar-content {
        background-color: #0077B5;
        color: #ffffff;
        border-radius: 15px;
        padding: 20px;
    }

    .css-1d391kg, .css-2trqyj {
        color: #ffffff !important;
    }

    .stButton>button {
        color: white;
        background-color: #0077B5;
        border-radius: 15px;
        transition: background-color 0.5s ease;
    }

    .stButton>button:hover {
        background-color: #005f8b;
    }

    .stMetric {
        text-align: center;
        font-size: 1.5em;
        border-radius: 15px;
        padding: 10px;
        background-color: #ffffff;
        margin: 10px;
    }

    .stMetric > div {
        transition: transform 0.5s ease;
    }

    .stMetric:hover > div {
        transform: scale(1.05);
    }

    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar components
min_date = day_df["dateday"].min()
max_date = day_df["dateday"].max()

st.sidebar.image("https://jugnoo.io/wp-content/uploads/2022/05/on-demand-bike-sharing-1-1024x506.jpg", use_column_width=True)
st.sidebar.header("Filter:")

# Date range filter
start_date, end_date = st.sidebar.date_input(
    label="Date Range",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

st.sidebar.header("Connect with me:")
st.sidebar.markdown("Fahru Rojak")

# Social media links
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://id.linkedin.com/in/fahrurojak?trk=public_profile_browsemap)")
st.sidebar.markdown("For inquiries and collaborations, feel free to contact me!")
st.sidebar.markdown("Keep riding and stay healthy!")
st.sidebar.markdown("---")
st.sidebar.markdown("[Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)")

# Filtering data based on date range
main_df = day_df[
    (day_df["dateday"] >= pd.to_datetime(start_date)) &
    (day_df["dateday"] <= pd.to_datetime(end_date))
]

# Main title and metrics
st.title("🚲 Bike Sharing Dashboard 🚲")
st.markdown("##")

col1, col2, col3 = st.columns(3)

# Metrics
with col1:
    total_all_rides = main_df['count'].sum()
    st.metric("Total Rides", value=total_all_rides)

with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)

with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

# Visualizations
# Monthly rental trends
monthly_rent_df['total_rides'] = monthly_rent_df['casual_rides'] + monthly_rent_df['registered_rides']
fig = px.bar(monthly_rent_df,
             x='yearmonth',
             y=['casual_rides', 'registered_rides', 'total_rides'],
             barmode='group',
             color_discrete_sequence=["#FF69B4", "#00FF00", "#0000FF"],
             title="Bike Rental Trends in Recent Years",
             labels={'casual_rides': 'Casual Rentals', 'registered_rides': 'Registered Rentals', 'total_rides': 'Total Rides'})

fig.update_layout(
    xaxis_title='',
    yaxis_title='Total Rentals',
    xaxis=dict(showgrid=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
    yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
    plot_bgcolor='rgba(255, 255, 255, 0)',
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# Weather distribution
fig = px.box(day_df, x='weathersit', y='count', color='weathersit', 
             title='Bike Users Distribution Based on Weather Condition',
             labels={'weathersit': 'Weather Condition', 'count': 'Total Rentals'})

st.plotly_chart(fig, use_container_width=True)

# Working day rental clusters
fig1 = px.box(day_df, x='workingday', y='count', color='workingday',
              title='Bike Rental Clusters by Working Day',
              labels={'workingday': 'Working Day', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF'])
fig1.update_xaxes(title_text='Working Day')
fig1.update_yaxes(title_text='Total Rentals')

# Holiday rental clusters
fig2 = px.box(day_df, x='holiday', y='count', color='holiday',
              title='Bike Rental Clusters by Holiday',
              labels={'holiday': 'Holiday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF'])
fig2.update_xaxes(title_text='Holiday')
fig2.update_yaxes(title_text='Total Rentals')

# Weekday rental clusters
fig3 = px.box(day_df, x='weekday', y='count', color='weekday',
              title='Bike Rental Clusters by Weekday',
              labels={'weekday': 'Weekday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF'])
fig3.update_xaxes(title_text='Weekday')
fig3.update_yaxes(title_text='Total Rentals')

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# Temperature scatter plot
fig = px.scatter(day_df, x='temp', y='count', color='season',
                 title='Bike Rental Clusters by Season and Temperature',
                 labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 hover_name='season')

st.plotly_chart(fig, use_container_width=True)

# Seasonal rental counts
seasonal_usage = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()

fig = px.bar(seasonal_usage, x='season', y=['registered', 'casual'],
             title='Bike Rental Counts by Season',
             labels={'season': 'Season', 'value': 'Total Rentals', 'variable': 'User Type'},
             color_discrete_sequence=["#00FF00","#0000FF"], barmode='group')

st.plotly_chart(fig, use_container_width=True)

st.caption('Copyright (c), created by Fahru Rojak')
