import os
import requests
import pandas as pd

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

# If the CSV already exists, load it and append only new rows
if os.path.exists(csv_filename):
    existing_df = pd.read_csv(csv_filename)
    # Assuming the first column is 'date_time', filter out duplicate timestamps.
    new_data = weather_stats[~weather_stats.iloc[:, 0].isin(existing_df.iloc[:, 0])]
    if not new_data.empty:
        new_data.to_csv(csv_filename, mode='a', header=False, index=False)
    else:
        print("No new data to append.")
else:
    weather_stats.to_csv(csv_filename, index=False)