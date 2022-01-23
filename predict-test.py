import requests
from datetime import datetime
url = 'http://localhost:9999/predict'

# If request-weather-data is True you
# must have a valid API key 
# See get_weather_features.py for details


wind_res = {"date": "2021-11-07",
             "request-weather-data": False
            }
print(wind_res)
response = requests.post(url, json=wind_res).json()
print(response)

