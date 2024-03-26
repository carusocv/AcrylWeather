import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

#Setup for the API
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


# Simple API URL + function to query the weather API
url = "https://api.open-meteo.com/v1/forecast"
def query_weather_api(longitudes, latitudes):
    if not longitudes or not latitudes:
        raise ValueError("Error: No coordinates provided.")
    else: 
        # Just creating the Open-Meteo API client
        openmeteo = openmeteo_requests.Client()

        # Define the parameters for the API call
        # This is what I talked about on line #13 of main. The API wants a list of latitudes and longitudes.
        params = {
            "latitude": latitudes,
            "longitude": longitudes,
            "current": ["temperature_2m", "wind_speed_10m"],
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "PST"  # Specify the timezone as PST
        }

        # Make the API call
        responses = openmeteo.weather_api(url, params=params)

    return responses 
