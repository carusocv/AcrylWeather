import datetime

import weather_api
import google_sheets

def main():
    # On main call we want to first read the coordinates fro the google sheet. 
    read_coordinates = google_sheets.read_coordinates()

    # if we get coordinates back, we want to query the weather api and eventually update the sheet.
    if read_coordinates:
        # We returned a tuple of latitudes and longitudes so we are gong to unpack them into two lists
        # This is for the structure of the weather API which wants to take in a list of latitudes and longitudes
        latitudes, longitudes = zip(*read_coordinates)

        # Query the weather API for the given coordinates
        responses = weather_api.query_weather_api(list(longitudes), list(latitudes))

        # Light logic here, could very well move this to write_weather_data
        # Mostly kept this here to keep the scope of read_coordinates to this file.
        
        # Setting values list and then appending each of the weather stats
        values = []
        for response, (latitude, longitude) in zip(responses, read_coordinates):
            current = response.Current()
            # Update temperature to the nearest whole number + '°F'
            temperature = str(round(current.Variables(0).Value())) + '°F'
            # Update wind speed to one decimal place + ' mph'
            wind_speed = "{:.1f}".format(current.Variables(1).Value()) + ' mph'
            # Convert timestamp to datetime object
            last_updated = datetime.datetime.fromtimestamp(current.Time()).strftime('%Y-%m-%d %I:%M %p')

            values.append([temperature, wind_speed, last_updated])

        # Call the function to write weather data to Google Sheets
        google_sheets.write_weather_data(values)

if __name__ == "__main__":
    main()
