"""
Function to get data for the weather features using the DMI API
The uses needs to register an API KEY here:
https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111
The DMI_API_KEY is defined in my environment variables

This function uses the dmi_open_data library
https://github.com/LasseRegin/dmi-open-data
which makes the data download a lot easier

""" 
DMI_WEB_API="https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111"
import pandas as pd
from datetime import datetime
import os
import pandas as pd
import numpy as np
import sys
from dmi_open_data import DMIOpenDataClient, Parameter, ClimateDataParameter
import datetime as dt
feature_cols = ['WindMax', 'WindGustAlwaysPast1h', 'WindMin', 'WindMinPast1h', 'TempDew', 'Pressure', 'PressureAtSea', 'WindDirPast1h', 'TempDry', 'Weather', 'TempMeanPast1h', 'TempMaxPast1h', 'TempMinPast1h', 'Humidity', 'HumidityPast1h', 'Visibility']


# Setting the lat and lon to IKERMIT
def print_data(get_date,lat=64.780,lon=-40.300):
    # check if the API key is defined, otherwise fail
    check_api_key = os.getenv("DMI_API_KEY")
    if check_api_key is None:
        print("DMI_API_KEY not defined!")
        print(f"Please register in the DMI website: {DMI_WEB_API}")
        print("and add DMI_API_KEY to your env variables")
        return None
    client = DMIOpenDataClient(api_key=os.getenv('DMI_API_KEY'))
    stations = client.get_stations(limit=500)
    dmi_station = next(station for station in stations if station['properties']['name'].lower() == 'dmi')

    
    client = DMIOpenDataClient(api_key=os.getenv('DMI_API_KEY'))
    closest_station = client.get_closest_station( latitude=lat, longitude=lon)
    #print("Getting staion")
    #print(closest_station['properties'])
    this_date = get_date.split("-")
    if len(this_date) == 3: #user provided only YYYY-MM-DD
        year = int(this_date[0])
        month = int(this_date[1])
        day = int(this_date[2])
        from_time=datetime(year,month,day)
        to_time = from_time
    #elif len(this_date) == 4: #user provided also hour
    #    year = int(this_date[0])
    #    month = int(this_date[1])
    #    day = int(this_date[2])
    #    hour = int(this_date[3])
    #    from_time=datetime(year,month,day,hour)
    #    to_time = from_time
    #elif len(this_date) == 5: #user provided also hour and minutes
    #    year = int(this_date[0])
    #    month = int(this_date[1])
    #    day = int(this_date[2])
    #    hour = int(this_date[3])
    #    minute = int(this_date[4])
    #    from_time=datetime(year,month,day,hour,minute)
    #    to_time = from_time
    else:
        print("Number of parameters in time string is too long or too short!: {len(this_date)}")
        sys.exit(1)
    # Get available parameters
    #parameters = client.list_parameters()
    parameters = feature_cols
    #print(f"Selected {parameters}")

    print_features={}
    for param in parameters:
        allvals=[]
        alltimes=[]
        observations = client.get_observations(
            parameter=Parameter[param],
            station_id=dmi_station['properties']['stationId'],
            from_time=from_time,
            to_time=to_time,
            limit=200000)
        #I should only get one value!
        for obs in observations:
            value = obs["properties"]["value"]
            if param == 'Visibility': value = int(value)
            if param == 'Weather': value = int(value)
            time = obs["properties"]["observed"]
        #    allvals.append(value)
        #    alltimes.append(time)
        #time = observations["properties"]["observed"]
        print_features[param] =  [value]
        #print(f"{param}")
        #print(allvals)
        #print(time)
        #df=pd.DataFrame({param:allvals,"date":alltimes})
        #date1=datetime.strftime(from_time,"%Y%m%d")
        #date2=datetime.strftime(to_time,"%Y%m%d")
        #print(df)
        #df.to_csv("_".join([param,date1,date2])+".csv",index=False)
        #all_dfs.append(df)
    #print_features["time"] = time
    return print_features
