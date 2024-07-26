import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import streamlit as st

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/fahrurojak/Bike-Sharing_Dicoding/main/Dataset/day.csv")

# Remove irrelevant columns
day_df.drop(columns=['instant', 'windspeed'], inplace=True)

# Rename columns
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Change date format
day_df['dateday'] = pd.to_datetime(day_df['dateday'])
day_df['weekday'] = day_df['dateday'].dt.day_name()
day_df['year'] = day_df['dateday'].dt.year

# Map values to seasons and weather conditions
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Resample data by month
monthly_rent_df = day_df.resample('M', on='dateday').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
}).reset_index()
monthly_rent_df['dateday'] = monthly_rent_df['dateday'].dt.strftime('%b-%y')
monthly_rent_df.rename(columns={
    "dateday": "yearmonth",
    "count": "total_rides",
    "casual": "casual_rides",
    "registered": "registered_rides"
}, inplace=True)

# Aggregate statistics by month, weather, holiday, weekday, working day, and season
aggregated_stats_by_month = day_df.groupby('month')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_weather = day_df.groupby('weathersit')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_holiday = day_df.groupby('holiday')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_weekday = day_df.groupby('weekday')['count'].agg(['max', 'min', 'mean'])
aggregated_stats_by_workingday = day_df.groupby('workingday')['count'].agg(['max', 'min', 'mean'])
aggregated_stats_by_season = day_df.groupby('season').agg({
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# Sidebar filters and components
st.sidebar.image("placeholder-image.png")
st.sidebar.header("Filter:")
start_date, end_date = st.sidebar.date_input(
    label="Date",
    min_value=day_df["dateday"].min(),
    max_value=day_df["dateday"].max(),
    value=[day_df["dateday"].min(), day_df["dateday"].max()]
)
st.sidebar.header("Connect with me:")
st.sidebar.markdown("Fahru Rojak")
st.sidebar.markdown("[![LinkedIn]](https://id.linkedin.com/in/fahrurojak?trk=public_profile_browsemap)")
st.sidebar.markdown("For inquiries and collaborations, feel free to contact me!")
st.sidebar.markdown("Keep riding and stay healthy!")
st.sidebar.markdown("---")
st.sidebar.markdown("[Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)")

# Filter main data frame
main_df = day_df[
    (day_df["dateday"] >= str(start_date)) &
    (day_df["dateday"] <= str(end_date))
]

# Main page title and metrics
st.title("🚲 Bike Sharing Dashboard 🚲")
st.markdown("##")

col1, col2, col3 = st.columns(3)
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
monthly_rent_df['total_rides'] = monthly_rent_df['casual_rides'] + monthly_rent_df['registered_rides']
fig = px.bar(monthly_rent_df,
             x='yearmonth',
             y=['casual_rides', 'registered_rides', 'total_rides'],
             barmode='group',
             color_discrete_sequence=["#FF69B4", "#00FF00", "#0000FF"],
             title="Bike Rental Trends in Recent Years",
             labels={'casual_rides': 'Casual Rentals', 'registered_rides': 'Registered Rentals', 'total_rides': 'Total Rides'})
fig.update_layout(xaxis_title='', yaxis_title='Total Rentals',
                  xaxis=dict(showgrid=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  plot_bgcolor='rgba(255, 255, 255, 0)',
                  showlegend=True,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

fig = px.box(day_df, x='weathersit', y='count', color='weathersit', 
             title='Bike Users Distribution Based on Weather Condition',
             labels={'weathersit': 'Weather Condition', 'count': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

fig1 = px.box(day_df, x='workingday', y='count', color='workingday',
              title='Bike Rental Clusters by Working Day',
              labels={'workingday': 'Working Day', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig1.update_xaxes(title_text='Working Day')
fig1.update_yaxes(title_text='Total Rentals')
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.box(day_df, x='holiday', y='count', color='holiday',
              title='Bike Rental Clusters by Holiday',
              labels={'holiday': 'Holiday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig2.update_xaxes(title_text='Holiday')
fig2.update_yaxes(title_text='Total Rentals')
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.box(day_df, x='weekday', y='count', color='weekday',
              title='Bike Rental Clusters by Weekday',
              labels={'weekday': 'Weekday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig3.update_xaxes(title_text='Weekday')
fig3.update_yaxes(title_text='Total Rentals')
st.plotly_chart(fig3, use_container_width=True)

fig = px.scatter(day_df, x='temp', y='count', color='season',
                 title='Bike Rental Clusters by Season and Temperature',
                 labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 hover_name='season')
st.plotly_chart(fig, use_container_width=True)

seasonal_usage = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()
fig = px.bar(seasonal_usage, x='season', y=['registered', 'casual'],
             title='Bike Rental Counts by Season',
             labels={'season': 'Season', 'value': 'Total Rentals', 'variable': 'User Type'},
             color_discrete_sequence=["#00FF00","#0000FF"], barmode='group')
st.plotly_chart(fig, use_container_width=True)

st.caption('Copyright (c), created by Fahru Rojak')
