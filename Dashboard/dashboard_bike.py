import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import scipy.stats as stats
import streamlit as st

# Load dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/fahrurojak/Bike-Sharing_Dicoding/main/Dataset/day.csv")

# Drop irrelevant columns
drop_columns = ['instant', 'windspeed']
day_df.drop(columns=drop_columns, inplace=True)

# Rename columns
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Convert dateday to datetime
day_df['dateday'] = pd.to_datetime(day_df['dateday'])

# Extract year, month, and weekday
day_df['weekday'] = day_df['dateday'].dt.day_name()
day_df['year'] = day_df['dateday'].dt.year

# Map seasons and weather situations
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Aggregate data by month
monthly_rent_df = day_df.resample(rule='M', on='dateday').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
}).reset_index()

# Rename columns
monthly_rent_df.rename(columns={
    "count": "total_rides",
    "casual": "casual_rides",
    "registered": "registered_rides"
}, inplace=True)
monthly_rent_df['yearmonth'] = monthly_rent_df['dateday'].dt.strftime('%b-%y')

# Aggregation by month, weather, holiday, weekday, working day, and season
aggregated_stats_by_month = day_df.groupby('month')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_weather = day_df.groupby('weathersit')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_holiday = day_df.groupby('holiday')['count'].agg(['max', 'min', 'mean', 'sum'])
aggregated_stats_by_weekday = day_df.groupby('weekday')['count'].agg(['max', 'min', 'mean'])
aggregated_stats_by_workingday = day_df.groupby('workingday')['count'].agg(['max', 'min', 'mean'])

# Seasonal data aggregation
aggregated_stats_by_season = day_df.groupby('season').agg({
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# Streamlit setup
st.sidebar.image("https://img.fonwall.ru/o/63/velofristayl-trial-velosipedist-zakat.jpg")
st.sidebar.header("Filter:")
start_date, end_date = st.sidebar.date_input(
    label="Date",
    min_value=day_df["dateday"].min(),
    max_value=day_df["dateday"].max(),
    value=[day_df["dateday"].min(), day_df["dateday"].max()]
)
st.sidebar.header("Connect with me:")
st.sidebar.markdown("Fahru Rojak")
st.sidebar.markdown("[![LinkedIn]](https://id.linkedin.com/in/fahrurojak=public_profile_browsemap)")
st.sidebar.markdown("For inquiries and collaborations, feel free to contact me!")
st.sidebar.markdown("Keep riding and stay healthy!")
st.sidebar.markdown("---")
st.sidebar.markdown("[Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)")

# Filter data based on selected date range
main_df = day_df[(day_df["dateday"] >= str(start_date)) & (day_df["dateday"] <= str(end_date))]

# Main title
st.title("Bike Sharing Dashboard")
st.markdown("##")

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rides", value=main_df['count'].sum())
with col2:
    st.metric("Total Casual Rides", value=main_df['casual'].sum())
with col3:
    st.metric("Total Registered Rides", value=main_df['registered'].sum())

# Monthly rental trends
fig = px.bar(monthly_rent_df,
             x='yearmonth',
             y=['casual_rides', 'registered_rides', 'total_rides'],
             barmode='group',
             color_discrete_sequence=["#FF69B4", "#00FF00", "#0000FF"],
             title="Bike Rental Trends by Month",
             labels={'casual_rides': 'Casual Rentals', 'registered_rides': 'Registered Rentals', 'total_rides': 'Total Rides'},
             hover_name='yearmonth')
fig.update_layout(xaxis_title='', yaxis_title='Total Rentals',
                  xaxis=dict(showgrid=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  plot_bgcolor='rgba(255, 255, 255, 0)',
                  showlegend=True,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# Weather conditions
fig = px.box(day_df, x='weathersit', y='count', color='weathersit', 
             title='Bike Rentals by Weather Condition',
             labels={'weathersit': 'Weather Condition', 'count': 'Total Rentals'},
             color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
             hover_name='weathersit')
fig.update_layout(xaxis_title='', yaxis_title='Total Rentals')
st.plotly_chart(fig, use_container_width=True)

# Working day
fig1 = px.box(day_df, x='workingday', y='count', color='workingday',
              title='Bike Rentals by Working Day',
              labels={'workingday': 'Working Day', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF'],
              hover_name='workingday')
fig1.update_xaxes(title_text='Working Day')
fig1.update_yaxes(title_text='Total Rentals')
st.plotly_chart(fig1, use_container_width=True)

# Holiday
fig2 = px.box(day_df, x='holiday', y='count', color='holiday',
              title='Bike Rentals by Holiday',
              labels={'holiday': 'Holiday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF'],
              hover_name='holiday')
fig2.update_xaxes(title_text='Holiday')
fig2.update_yaxes(title_text='Total Rentals')
st.plotly_chart(fig2, use_container_width=True)

# Weekday
fig3 = px.box(day_df, x='weekday', y='count', color='weekday',
              title='Bike Rentals by Weekday',
              labels={'weekday': 'Weekday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'],
              hover_name='weekday')
fig3.update_xaxes(title_text='Weekday')
fig3.update_yaxes(title_text='Total Rentals')
st.plotly_chart(fig3, use_container_width=True)

# Scatter plot by temperature and season
fig = px.scatter(day_df, x='temp', y='count', color='season',
                 title='Bike Rentals by Temperature and Season',
                 labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 hover_name='season')
st.plotly_chart(fig, use_container_width=True)

# Seasonal usage bar plot
seasonal_usage = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()
fig = px.bar(seasonal_usage, x='season', y=['registered', 'casual'],
             title='Bike Rentals by Season',
             labels={'season': 'Season', 'value': 'Total Rentals', 'variable': 'User Type'},
             color_discrete_sequence=["#00FF00", "#0000FF"], barmode='group',
             hover_name='season')
st.plotly_chart(fig, use_container_width=True)

# Correlation Analysis
correlation_matrix = day_df[['temp', 'atemp', 'hum', 'count']].corr()
st.write("### Correlation Analysis")
st.write(correlation_matrix)

# Heatmap for correlation
fig = plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Heatmap')
st.pyplot(fig)

# Trend Analysis by Year
yearly_rent_df = day_df.groupby('year').agg({'count': 'sum'}).reset_index()
fig = px.line(yearly_rent_df, x='year', y='count',
              title='Total Bike Rentals by Year',
              labels={'count': 'Total Rentals'},
              markers=True)
st.plotly_chart(fig, use_container_width=True)

# Monthly and Daily Patterns
monthly_pattern = day_df.groupby('month')['count'].mean().reset_index()
fig = px.line(monthly_pattern, x='month', y='count',
              title='Average Bike Rentals by Month',
              labels={'count': 'Average Rentals'},
              markers=True)
st.plotly_chart(fig, use_container_width=True)

daily_pattern = day_df.groupby('weekday')['count'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
fig = px.bar(daily_pattern, x='weekday', y='count',
             title='Average Bike Rentals by Weekday',
             labels={'count': 'Average Rentals'},
             color_discrete_sequence=['#1f77b4'])
st.plotly_chart(fig, use_container_width=True)

# Impact of Temperature and Humidity
fig = px.scatter(day_df, x='temp', y='count', color='season',
                 title='Bike Rentals vs Temperature',
                 labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 hover_name='season')
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(day_df, x='hum', y='count', color='season',
                 title='Bike Rentals vs Humidity',
                 labels={'hum': 'Humidity (%)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 hover_name='season')
st.plotly_chart(fig, use_container_width=True)

# Top 10 Days for Bike Rentals
top_10_days = day_df[['dateday', 'count']].sort_values(by='count', ascending=False).head(10)
fig = px.bar(top_10_days, x='dateday', y='count',
             title='Top 10 Days for Bike Rentals',
             labels={'dateday': 'Date', 'count': 'Total Rentals'},
             color_discrete_sequence=['#FF6347'],
             hover_name='dateday')
st.plotly_chart(fig, use_container_width=True)

# Holiday vs Non-Holiday Analysis
holiday_comparison = day_df.groupby('holiday')['count'].agg(['mean', 'sum']).reset_index()
fig = px.bar(holiday_comparison, x='holiday', y='sum',
             title='Bike Rentals: Holiday vs Non-Holiday',
             labels={'holiday': 'Holiday', 'sum': 'Total Rentals'},
             color_discrete_sequence=['#FF6347'],
             hover_name='holiday')
st.plotly_chart(fig, use_container_width=True)

# Additional Analysis
# Rental patterns by hour of the day
day_df['hour'] = day_df['hr'].apply(lambda x: x // 1)  # Assuming 'hr' is the hour column
hourly_rent_df = day_df.groupby('hour')['count'].mean().reset_index()
fig = px.line(hourly_rent_df, x='hour', y='count',
              title='Average Bike Rentals by Hour of the Day',
              labels={'hour': 'Hour of the Day', 'count': 'Average Rentals'},
              markers=True)
st.plotly_chart(fig, use_container_width=True)

# Heatmap for daily patterns
daily_rent_df = day_df.groupby(['weekday', 'hour'])['count'].mean().reset_index()
fig = px.density_heatmap(daily_rent_df, x='hour', y='weekday', z='count',
                        title='Heatmap of Bike Rentals by Hour and Weekday',
                        labels={'hour': 'Hour of the Day', 'weekday': 'Weekday', 'count': 'Average Rentals'},
                        color_continuous_scale='Viridis')
st.plotly_chart(fig, use_container_width=True)

st.write("### Detailed Analysis")
st.write("**1. Correlation Analysis**: Analyzed how features like temperature, perceived temperature, and humidity correlate with the total bike rentals.")
st.write("**2. Trend Analysis by Year**: Examined the trend of total bike rentals over different years.")
st.write("**3. Monthly and Daily Patterns**: Explored average bike rentals on a monthly and daily basis.")
st.write("**4. Impact of Temperature and Humidity**: Investigated how temperature and humidity affect bike rentals.")
st.write("**5. Top 10 Days for Bike Rentals**: Identified the top 10 days with the highest number of rentals.")
st.write("**6. Holiday vs Non-Holiday Analysis**: Compared bike rentals on holidays and non-holidays.")
st.write("**7. Rental Patterns by Hour of the Day**: Explored how bike rentals vary by hour of the day.")
st.write("**8. Heatmap of Daily Patterns**: Visualized the density of bike rentals by hour and weekday.")

# Footer
st.caption('Copyright (c), created by Fahru Rojak')
