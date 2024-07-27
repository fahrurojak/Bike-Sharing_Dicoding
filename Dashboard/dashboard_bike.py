# Libraries Used
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

# LinkedIn
st.sidebar.markdown(
    "[![LinkedIn](https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg)](https://id.linkedin.com/in/fahrurojak=public_profile_browsemap)"
)

# Instagram
st.sidebar.markdown(
    '<a href="https://www.instagram.com/your_instagram_profile" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30" height="30" alt="Instagram"/></a>',
    unsafe_allow_html=True
)

# GitHub
st.sidebar.markdown(
    '<a href="https://github.com/your_github_profile" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" width="30" height="30" alt="GitHub"/></a>',
    unsafe_allow_html=True
)

st.sidebar.markdown("Jika Anda memiliki pertanyaan atau tertarik untuk berkolaborasi, jangan ragu untuk menghubungi saya melalui media sosial.")
st.sidebar.markdown("Semoga Anda terus bersemangat dalam beraktivitas dan selalu menjaga kesehatan dengan baik!")
st.sidebar.markdown("---")
st.sidebar.markdown("[Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)")

# Adding some custom CSS for animation
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content a img {
        transition: transform 0.3s;
    }
    .sidebar .sidebar-content a img:hover {
        transform: scale(1.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
             labels={'casual_rides': 'Casual Rentals', 'registered_rides': 'Registered Rentals', 'total_rides': 'Total Rides'})
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
             labels={'weathersit': 'Weather Condition', 'count': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Working day
fig1 = px.box(day_df, x='workingday', y='count', color='workingday',
              title='Bike Rentals by Working Day',
              labels={'workingday': 'Working Day', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF'])
fig1.update_xaxes(title_text='Working Day')
fig1.update_yaxes(title_text='Total Rentals')

# Holiday
fig2 = px.box(day_df, x='holiday', y='count', color='holiday',
              title='Bike Rentals by Holiday',
              labels={'holiday': 'Holiday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF'])
fig2.update_xaxes(title_text='Holiday')
fig2.update_yaxes(title_text='Total Rentals')

# Weekday
fig3 = px.box(day_df, x='weekday', y='count', color='weekday',
              title='Bike Rentals by Weekday',
              labels={'weekday': 'Weekday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig3.update_xaxes(title_text='Weekday')
fig3.update_yaxes(title_text='Total Rentals')

# Scatter plot by temperature and season
fig = px.scatter(day_df, x='temp', y='count', color='season',
                 title='Bike Rentals by Temperature and Season',
                 labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
st.plotly_chart(fig, use_container_width=True)

# Seasonal usage bar plot
seasonal_usage = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()
fig = px.bar(seasonal_usage, x='season', y=['registered', 'casual'],
             title='Bike Rentals by Season',
             labels={'season': 'Season', 'value': 'Total Rentals', 'variable': 'User Type'},
             color_discrete_sequence=["#00FF00", "#0000FF"], barmode='group')
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
              labels={'count': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Monthly and Daily Patterns
monthly_pattern = day_df.groupby('month')['count'].mean().reset_index()
fig = px.line(monthly_pattern, x='month', y='count',
              title='Average Bike Rentals by Month',
              labels={'count': 'Average Rentals'})
st.plotly_chart(fig, use_container_width=True)

daily_pattern = day_df.groupby('weekday')['count'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
fig = px.bar(daily_pattern, x='weekday', y='count',
             title='Average Bike Rentals by Weekday',
             labels={'count': 'Average Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Impact of Temperature and Humidity
fig = px.scatter(day_df, x='temp', y='count', color='season',
                 title='Bike Rentals vs Temperature',
                 labels={'temp': 'Temperature (°C)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(day_df, x='hum', y='count', color='season',
                 title='Bike Rentals vs Humidity',
                 labels={'hum': 'Humidity (%)', 'count': 'Total Rentals'},
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
st.plotly_chart(fig, use_container_width=True)

# Top 10 Days for Bike Rentals
top_10_days = day_df[['dateday', 'count']].sort_values(by='count', ascending=False).head(10)
fig = px.bar(top_10_days, x='dateday', y='count',
             title='Top 10 Days for Bike Rentals',
             labels={'dateday': 'Date', 'count': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Holiday vs Non-Holiday Analysis
holiday_comparison = day_df.groupby('holiday')['count'].agg(['mean', 'sum']).reset_index()
fig = px.bar(holiday_comparison, x='holiday', y='sum',
             title='Bike Rentals: Holiday vs Non-Holiday',
             labels={'holiday': 'Holiday', 'sum': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Hourly Ride Patterns
# Extract hour from the 'dateday' column
day_df['hour'] = day_df['dateday'].dt.hour

# Aggregate data by hour
hourly_rent_df = day_df.groupby('hour').agg({'count': 'sum'}).reset_index()

# Hourly ride patterns
fig = px.line(hourly_rent_df, x='hour', y='count',
              title='Hourly Bike Rentals',
              labels={'hour': 'Hour of Day', 'count': 'Total Rentals'})
fig.update_xaxes(tickmode='linear')
st.plotly_chart(fig, use_container_width=True)

# Weather Impact Analysis
# Aggregate data by weather condition
weather_impact_df = day_df.groupby('weathersit').agg({'count': 'mean'}).reset_index()

# Weather impact
fig = px.bar(weather_impact_df, x='weathersit', y='count',
             title='Average Bike Rentals by Weather Condition',
             labels={'weathersit': 'Weather Condition', 'count': 'Average Rentals'},
             color='count', color_continuous_scale='Viridis')
st.plotly_chart(fig, use_container_width=True)

# Correlation with Weather Conditions
# Add weather conditions to correlation matrix
correlation_matrix_extended = day_df[['temp', 'atemp', 'hum', 'count', 'weathersit']].copy()
correlation_matrix_extended = pd.get_dummies(correlation_matrix_extended, columns=['weathersit'])
correlation_matrix_extended = correlation_matrix_extended.corr()

# Extended Correlation Heatmap
fig = plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix_extended, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Extended Correlation Heatmap')
st.pyplot(fig)

# Monthly and Seasonal Trends with Interactive Visualizations
# Monthly trends
fig = px.line(monthly_rent_df, x='yearmonth', y='total_rides',
              title='Monthly Bike Rental Trends',
              labels={'total_rides': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Seasonal comparison
seasonal_comparison = day_df.groupby('season').agg({'count': 'mean'}).reset_index()
fig = px.pie(seasonal_comparison, names='season', values='count',
             title='Bike Rentals by Season',
             labels={'count': 'Average Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Ride Trends by Working Day and Holiday
# Working Day vs Holiday Analysis
working_vs_holiday = day_df.groupby(['workingday', 'holiday']).agg({'count': 'mean'}).reset_index()
fig = px.bar(working_vs_holiday, x='workingday', y='count', color='holiday',
             title='Bike Rentals by Working Day and Holiday',
             labels={'workingday': 'Working Day', 'count': 'Average Rentals'})
st.plotly_chart(fig, use_container_width=True)


# Footer
st.caption('Copyright (c), created by Fahru Rojak')
