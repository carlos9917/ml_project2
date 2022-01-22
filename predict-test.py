import requests
from datetime import datetime
url = 'http://localhost:9999/predict'

wind_date = {"date": "2021-11-07"
            }

response = requests.post(url, json=wind_date).json()
print(response)

