# Libraries Used
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.ensemble import RandomForestRegressor
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
# Weekday, month, year columns
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

# Grouping bike renters (casual and registered) data by month
grouped_by_month = day_df.groupby('month')
aggregated_stats_by_month = grouped_by_month['count'].agg(['max', 'min', 'mean', 'sum'])

# Grouping bike renters (casual and registered) data by weather
grouped_by_weather = day_df.groupby('weathersit')
aggregated_stats_by_weather = grouped_by_weather['count'].agg(['max', 'min', 'mean', 'sum'])

# Grouping bike renters (casual and registered) data by holiday
grouped_by_holiday = day_df.groupby('holiday')
aggregated_stats_by_holiday = grouped_by_holiday['count'].agg(['max', 'min', 'mean', 'sum'])

# Comparing the number of bike renters on weekdays and weekends
grouped_by_weekday = day_df.groupby('weekday')
aggregated_stats_by_weekday = grouped_by_weekday['count'].agg(['max', 'min', 'mean'])

# Grouping bike renters data by working day
grouped_by_workingday = day_df.groupby('workingday')
aggregated_stats_by_workingday = grouped_by_workingday['count'].agg(['max', 'min', 'mean'])

# Grouping data by season and calculating aggregate statistics for temperature variables (temp),
# perceived temperature (atemp),
# and humidity (hum)
aggregated_stats_by_season = day_df.groupby('season').agg({
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# Prepare filter components
min_date = day_df["dateday"].min()
max_date = day_df["dateday"].max()

# Sidebar
st.sidebar.image("https://img.fonwall.ru/o/63/velofristayl-trial-velosipedist-zakat.jpg")
st.sidebar.header("Filter:")
start_date, end_date = st.sidebar.date_input(
    label="Date",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)
st.sidebar.header("Connect with me:")
st.sidebar.markdown("Fahru Rojak")
col1 = st.sidebar
with col1:
    st.markdown("[![LinkedIn]](https://id.linkedin.com/in/fahrurojak=public_profile_browsemap)")
st.sidebar.markdown("For inquiries and collaborations, feel free to contact me!")
st.sidebar.markdown("Keep riding and stay healthy!")
st.sidebar.markdown("---")
st.sidebar.markdown("[Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)")

# Filter main_df
main_df = day_df[
    (day_df["dateday"] >= str(start_date)) &
    (day_df["dateday"] <= str(end_date))
]

# Main Page
st.title("Bike Sharing Dashboard")
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

# Grouping data by yearmonth and calculating the total casual, registered, and total rides
monthly_rent_df['total_rides'] = monthly_rent_df['casual_rides'] + monthly_rent_df['registered_rides']
fig = px.bar(monthly_rent_df,
             x='yearmonth',
             y=['casual_rides', 'registered_rides', 'total_rides'],
             barmode='group',
             color_discrete_sequence=["#FF69B4", "#00FF00", "#0000FF"],
             title="Bike Rental Trends in Recent Years",
             labels={'casual_rides': 'Casual Rentals', 'registered_rides': 'Registered Rentals', 'total_rides': 'Total Rides'})

# Displaying the figure
fig.update_layout(xaxis_title='', yaxis_title='Total Rentals',
                  xaxis=dict(showgrid=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  plot_bgcolor='rgba(255, 255, 255, 0)',
                  showlegend=True,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# Weather
fig = px.box(day_df, x='weathersit', y='count', color='weathersit', 
             title='Bike Users Distribution Based on Weather Condition',
             labels={'weathersit': 'Weather Condition', 'count': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

# Plot for working day
fig1 = px.box(day_df, x='workingday', y='count', color='workingday',
              title='Bike Rental Clusters by Working Day',
              labels={'workingday': 'Working Day', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig1.update_xaxes(title_text='Working Day')
fig1.update_yaxes(title_text='Total Rentals')

# Plot for holiday
fig2 = px.box(day_df, x='holiday', y='count', color='holiday',
              title='Bike Rental Clusters by Holiday',
              labels={'holiday': 'Holiday', 'count': 'Total Rentals'},
              color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0000'])
fig2.update_xaxes(title_text='Holiday')
fig2.update_yaxes(title_text='Total Rentals')

# Combining the two plots
combined_fig = fig1
combined_fig.add_traces(fig2.data)
st.plotly_chart(combined_fig, use_container_width=True)

# Plot for weekday
fig3 = px.box(day_df, x='weekday', y='count', color='weekday',
              title='Bike Rental Clusters by Weekday',
              labels={'weekday': 'Weekday', 'count': 'Total Rentals'},
              color_discrete_sequence=px.colors.qualitative.Set3)
fig3.update_xaxes(title_text='Weekday')
fig3.update_yaxes(title_text='Total Rentals')
st.plotly_chart(fig3, use_container_width=True)

# Time Series Decomposition
ts_decomposition = seasonal_decompose(day_df.set_index('dateday')['count'], model='multiplicative')
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
ts_decomposition.observed.plot(ax=ax1, legend=False)
ax1.set_ylabel('Observed')
ts_decomposition.trend.plot(ax=ax2, legend=False)
ax2.set_ylabel('Trend')
ts_decomposition.seasonal.plot(ax=ax3, legend=False)
ax3.set_ylabel('Seasonal')
ts_decomposition.resid.plot(ax=ax4, legend=False)
ax4.set_ylabel('Residual')
ax4.set_xlabel('Date')
fig.suptitle('Time Series Decomposition of Bike Rentals', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(fig)

# Correlation Heatmap
corr_matrix = day_df.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap of Bike Rental Dataset', fontsize=16)
st.pyplot(plt)

# Feature Importance using Random Forest
X = day_df.drop(columns=['count', 'dateday'])
y = day_df['count']
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)
feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
plt.figure(figsize=(12, 8))
feature_importances.plot(kind='bar', color='#1B9154')
plt.title('Feature Importance based on Random Forest', fontsize=16)
plt.xlabel('Features')
plt.ylabel('Importance')
st.pyplot(plt)
