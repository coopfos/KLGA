import os
import requests
import pandas as pd
from datetime import datetime

# Define the URL for weather station data
url = (
    "https://api.mesowest.net/v2/stations/timeseries?STID=KLGA"
    "&showemptystations=1&units=temp|F,speed|mph,english"
    "&recent=4320&token=d8c6aee36a994f90857925cea26934be"
    "&complete=1&obtimezone=local"
)

# Fetch the data from the API
response = requests.get(url)
station_data = response.json()["STATION"][0]["OBSERVATIONS"]

# Build a DataFrame from selected observations
stats = [
    station_data.get("date_time"),
    station_data.get("air_temp_set_1"),
    station_data.get("relative_humidity_set_1"),
    station_data.get("wind_speed_set_1"),
    station_data.get("wind_gust_set_1"),
    station_data.get("cloud_layer_1_code_set_1"),
]
df = pd.DataFrame(stats).transpose()

# Assign simplified, snake_case column names
df.columns = [
    "date_time",
    "air_temp",
    "humidity",
    "wind_speed",
    "wind_gust",
    "cloud_layer_code",
]

# Add a new column with the current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df["data_added_at"] = timestamp

csv_filename = "weather_data.csv"

if os.path.exists(csv_filename):
    # Load the existing CSV data
    existing_df = pd.read_csv(csv_filename)
    # Filter the new DataFrame for rows that are not already in the CSV based on 'date_time'
    new_data = df[~df["date_time"].isin(existing_df["date_time"])]
    if not new_data.empty:
        new_data.to_csv(csv_filename, mode="a", header=False, index=False)
        print("Appended new data with timestamp.")
    else:
        print("No new data to append.")
else:
    # If no CSV exists, create it with headers
    df.to_csv(csv_filename, index=False)
    print("Created new CSV with initial data.")