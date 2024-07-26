# Importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
import streamlit as st

# Reading the dataset
day_df = pd.read_csv('/mnt/data/day.csv')

# Displaying the first few rows of the dataset
st.write(day_df.head())

# Data Cleaning and Preprocessing
# Removing unnecessary columns
drop_columns = ['instant', 'windspeed']
day_df.drop(columns=drop_columns, inplace=True)

# Renaming columns for better readability
day_df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Converting date column to datetime
day_df['date'] = pd.to_datetime(day_df['date'])

# Extracting weekday and year information
day_df['weekday'] = day_df['date'].dt.day_name()
day_df['year'] = day_df['date'].dt.year

# Mapping season and weather conditions to descriptive names
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Displaying the cleaned dataset
st.write(day_df.head())

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
        background-color: #ffffff;
        color: #333333;
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
    }

    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        color: #333333;
        border-radius: 15px;
        padding: 20px;
    }

    .css-1d391kg, .css-2trqyj {
        color: #0077B5 !important;
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
        background-color: #f8f9fa;
        margin: 10px;
    }

    .stMetric > div {
        transition: transform 0.5s ease;
    }

    .stMetric:hover > div {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Basic Statistical Analysis
st.write("### Basic Statistical Analysis")
st.write(day_df.describe())

# Missing values analysis
st.write("### Missing Values Analysis")
st.write(day_df.isnull().sum())

# Temporal Analysis
st.write("### Temporal Analysis")

# Monthly trends
monthly_rentals = day_df.resample('M', on='date')['count'].sum().reset_index()
fig_monthly = px.line(monthly_rentals, x='date', y='count', title='Monthly Bike Rentals')
st.plotly_chart(fig_monthly, use_container_width=True)

# Yearly trends
yearly_rentals = day_df.groupby('year')['count'].sum().reset_index()
fig_yearly = px.bar(yearly_rentals, x='year', y='count', title='Yearly Bike Rentals')
st.plotly_chart(fig_yearly, use_container_width=True)

# Daily trends
fig_daily = px.line(day_df, x='date', y='count', title='Daily Bike Rentals')
st.plotly_chart(fig_daily, use_container_width=True)

# Categorical Analysis
st.write("### Categorical Analysis")

# Rentals by season
season_rentals = day_df.groupby('season')['count'].sum().reset_index()
fig_season = px.bar(season_rentals, x='season', y='count', title='Bike Rentals by Season', color='season')
st.plotly_chart(fig_season, use_container_width=True)

# Rentals by weekday
weekday_rentals = day_df.groupby('weekday')['count'].sum().reset_index()
fig_weekday = px.bar(weekday_rentals, x='weekday', y='count', title='Bike Rentals by Weekday', color='weekday')
st.plotly_chart(fig_weekday, use_container_width=True)

# Rentals by weather conditions
weather_rentals = day_df.groupby('weathersit')['count'].sum().reset_index()
fig_weather = px.bar(weather_rentals, x='weathersit', y='count', title='Bike Rentals by Weather Conditions', color='weathersit')
st.plotly_chart(fig_weather, use_container_width=True)

# Rentals on holidays vs. working days
holiday_rentals = day_df.groupby('holiday')['count'].sum().reset_index()
fig_holiday = px.bar(holiday_rentals, x='holiday', y='count', title='Bike Rentals on Holidays vs. Working Days', color='holiday')
st.plotly_chart(fig_holiday, use_container_width=True)

# Correlation Analysis
st.write("### Correlation Analysis")
corr_matrix = day_df.corr()
fig_corr = plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
st.pyplot(fig_corr)

# Impact Analysis
st.write("### Impact Analysis")

# Impact of temperature on bike rentals
fig_temp = px.scatter(day_df, x='temp', y='count', color='season', title='Impact of Temperature on Bike Rentals', trendline='ols')
st.plotly_chart(fig_temp, use_container_width=True)

# Impact of humidity on bike rentals
fig_humidity = px.scatter(day_df, x='hum', y='count', color='season', title='Impact of Humidity on Bike Rentals', trendline='ols')
st.plotly_chart(fig_humidity, use_container_width=True)

# Impact of weather conditions on bike rentals
fig_weather_impact = px.box(day_df, x='weathersit', y='count', color='weathersit', title='Impact of Weather Conditions on Bike Rentals')
st.plotly_chart(fig_weather_impact, use_container_width=True)

# Hourly analysis (if applicable)
st.write("### Hourly Analysis (if applicable)")
if 'hr' in day_df.columns:
    hourly_rentals = day_df.groupby('hr')['count'].sum().reset_index()
    fig_hourly = px.bar(hourly_rentals, x='hr', y='count', title='Hourly Bike Rentals', color='hr')
    st.plotly_chart(fig_hourly, use_container_width=True)

# Footer
st.caption('Copyright (c), created by Fahru Rojak')
