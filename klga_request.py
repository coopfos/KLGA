import os
import requests
import pandas as pd
from datetime import datetime

# URL for weather station data
url = 'https://api.mesowest.net/v2/stations/timeseries?STID=KLGA&showemptystations=1&units=temp|F,speed|mph,english&recent=4320&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local'

# Fetch the data
weather_req = requests.get(url)
station_data = weather_req.json().get("STATION")[0].get("OBSERVATIONS")

# Build a DataFrame from selected observations
stats = [
    station_data.get("date_time"), 
    station_data.get("air_temp_set_1"),
    station_data.get("relative_humidity_set_1"),
    station_data.get("wind_speed_set_1"),
    station_data.get("wind_gust_set_1"),
    station_data.get("cloud_layer_1_code_set_1"),
]
weather_stats = pd.DataFrame(stats).transpose()

csv_filename = "weather_data.csv"

# If the CSV exists, append only new data with timestamp
if os.path.exists(csv_filename):
    existing_df = pd.read_csv(csv_filename)
    # Filter for rows with date_time values not in existing CSV
    new_data = weather_stats[~weather_stats['date_time'].isin(existing_df['date_time'])]
    if not new_data.empty:
        # Add a column with the current timestamp
        new_data['data_added_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Append the new data to the CSV file (without writing header)
        new_data.to_csv(csv_filename, mode='a', header=False, index=False)
        print("Appended new data.")
    else:
        print("No new data to append.")
else:
    # For the first run, add the timestamp column and create the CSV file
    weather_stats['data_added_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_stats.to_csv(csv_filename, index=False)
    print("Created new CSV with initial data.")