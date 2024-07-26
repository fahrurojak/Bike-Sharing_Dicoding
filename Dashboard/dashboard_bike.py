# Importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
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

# Resampling data based on month and calculating total rides
monthly_rent_df = day_df.resample(rule='M', on='date').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
}).reset_index()

# Change index format to month-year (Jan-20, Feb-20, etc.)
monthly_rent_df['date'] = monthly_rent_df['date'].dt.strftime('%b-%y')

# Rename columns for clarity
monthly_rent_df.rename(columns={
    "date": "yearmonth",
    "count": "total_rides",
    "casual": "casual_rides",
    "registered": "registered_rides"
}, inplace=True)

# Aggregating statistics by different groupings
aggregated_stats_by_month = day_df.groupby('month')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_weather = day_df.groupby('weathersit')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_holiday = day_df.groupby('holiday')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_weekday = day_df.groupby('weekday')['count'].agg(['max', 'min', 'mean'])
aggregated_stats_by_workingday = day_df.groupby('workingday')['count'].agg(['max', 'min', 'mean'])
aggregated_stats_by_season = day_df.groupby('season').agg({
    'casual': 'mean',
    'registered': 'mean',
    'count': ['max', 'min', 'mean']
})
seasonal_temp_hum = day_df.groupby('season').agg({
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# Data visualization
# Bar plot for monthly rental trends
fig1 = px.bar(monthly_rent_df,
             x='yearmonth',
             y=['casual_rides', 'registered_rides', 'total_rides'],
             barmode='group',
             color_discrete_sequence=["#FF69B4", "#00FF00", "#0000FF"],
             title="Bike Rental Trends in Recent Years",
             labels={'casual_rides': 'Casual Rentals', 'registered_rides': 'Registered Rentals', 'total_rides': 'Total Rides'})

st.plotly_chart(fig1, use_container_width=True)

# Box plot for bike users distribution based on weather condition
fig2 = px.box(day_df, x='weathersit', y='count', color='weathersit', 
             title='Bike Users Distribution Based on Weather Condition',
             labels={'weathersit': 'Weather Condition', 'count': 'Total Rentals'})

st.plotly_chart(fig2, use_container_width=True)

# Box plot for bike rental clusters by working day
fig3 = px.box(day_df, x='workingday', y='count', color='workingday',
              title='Bike Rental Clusters by Working Day',
              labels={'workingday': 'Working Day', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig3.update_xaxes(title_text='Working Day')
fig3.update_yaxes(title_text='Total Rentals')

# Box plot for bike rental clusters by holiday
fig4 = px.box(day_df, x='holiday', y='count', color='holiday',
              title='Bike Rental Clusters by Holiday',
              labels={'holiday': 'Holiday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig4.update_xaxes(title_text='Holiday')
fig4.update_yaxes(title_text='Total Rentals')

# Box plot for bike rental clusters by weekday
fig5 = px.box(day_df, x='weekday', y='count', color='weekday',
              title='Bike Rental Clusters by Weekday',
              labels={'weekday': 'Weekday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig5.update_xaxes(title_text='Weekday')
fig5.update_yaxes(title_text='Total Rentals')

# Displaying the plots
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)
st.plotly_chart(fig5, use_container_width=True)

# Scatter plot for bike rental clusters by season and temperature
fig6 = px.scatter(day_df, x='temp', y='count', color='season',
                 title='Bike Rental Clusters by Season and Temperature',
                 labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 hover_name='season')

st.plotly_chart(fig6, use_container_width=True)

# Bar plot for bike rental counts by season
seasonal_usage = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()
fig7 = px.bar(seasonal_usage, x='season', y=['registered', 'casual'],
             title='Bike Rental Counts by Season',
             labels={'season': 'Season', 'value': 'Total Rentals', 'variable': 'User Type'},
             color_discrete_sequence=["#00FF00","#0000FF"], barmode='group')

st.plotly_chart(fig7, use_container_width=True)

# New analysis: Bike rental patterns by temperature
fig8 = px.scatter(day_df, x='temp', y='count', color='season',
                  title='Bike Rental Patterns by Temperature and Season',
                  labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                  trendline='ols')

st.plotly_chart(fig8, use_container_width=True)

# New analysis: Correlation heatmap
corr_matrix = day_df.corr()
fig9 = plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
st.pyplot(fig9)

# Distribution of bike rentals by hour of the day
day_df['hour'] = day_df['date'].dt.hour
fig10 = px.histogram(day_df, x='hour', y='count', color='season',
                     title='Distribution of Bike Rentals by Hour of the Day',
                     labels={'hour': 'Hour of the Day', 'count': 'Total Rentals'},
                     nbins=24)
st.plotly_chart(fig10, use_container_width=True)

# Impact of humidity on bike rentals
fig11 = px.scatter(day_df, x='hum', y='count', color='season',
                   title='Impact of Humidity on Bike Rentals',
                   labels={'hum': 'Humidity', 'count': 'Total Rentals'},
                   trendline='ols')
st.plotly_chart(fig11, use_container_width=True)

# Trend of bike rentals over the years
fig12 = px.line(day_df, x='date', y='count', color='season',
                title='Trend of Bike Rentals Over the Years',
                labels={'date': 'Date', 'count': 'Total Rentals'})
st.plotly_chart(fig12, use_container_width=True)

# Displaying summary statistics
st.write('### Summary Statistics')
st.write(day_df.describe())

# Footer
st.caption('Copyright (c), created by Fahru Rojak')
