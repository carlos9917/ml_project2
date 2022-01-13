"""
script to get the data from DMI
The uses needs to register an API KEY here:
https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111
The DMI_API_KEY is defined in my environment variables
The scripts uses the dmi_open_data library
https://github.com/LasseRegin/dmi-open-data
which makes the data download a lot easier

""" 
DMI_WEB_API="https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111"

from datetime import datetime
import os
import pandas as pd
import numpy as np
import sys
from dmi_open_data import DMIOpenDataClient, Parameter, ClimateDataParameter
import datetime as dt

# check if the API key is defined, otherwise fail
check_api_key = os.getenv("DMI_API_KEY")
if check_api_key is None:
    print("DMI_API_KEY not defined!")
    print(f"Please register in the DMI website: {DMI_WEB_API}")
    print("and add DMI_API_KEY to your env variables")
    sys.exit(1)

# Get 10 stations
client = DMIOpenDataClient(api_key=os.getenv('DMI_API_KEY'))
stations = client.get_stations(limit=500)

# Get all stations
stations = client.get_stations()
# Get DMI station
dmi_station = next(
    station
    for station in stations
    if station['properties']['name'].lower() == 'dmi')

#IKERMIT
lat=64.780 
lon=-40.300

closest_station = client.get_closest_station(
    latitude=lat,
    longitude=lon)
print("Getting station")
print(closest_station['properties'])
from_time=datetime(2020,1,1)
to_time = datetime(2021,12,31)
# To convert to unix timestamp
ft = dt.datetime.strptime(dt.datetime.strftime(from_time,"%Y-%m-%d-%H:%M"), '%Y-%m-%d-%H:%M')
tt = dt.datetime.strptime(dt.datetime.strftime(to_time,"%Y-%m-%d-%H:%M"), '%Y-%m-%d-%H:%M')
ftt = int(ft.timestamp()*1000000)
ttt = int(tt.timestamp()*1000000)

# Get available parameters
parameters = client.list_parameters()
#Print parameters name
#for pam in parameters:
#    pname = pam["name"]
#    print(f"Parameter {pname}")

sel_params = [param["name"] for param in parameters if not any(x in param["name"] for x in ["1min","10min","12h","24h"])]
parameters = sel_params
#parameters=["TempDry", "TempDew", "Humidity", "Pressure", "PressureAtSea", "WindDir", "WindSpeed", "WindMax", "WindMin", "PrecipPast1h", "Visibility", "CloudCover", "CloudHeight", "Weather"]
parameters = sel_params
print(f"Selected {parameters}")


#parameters=["TempDry", "TempDew", "Humidity", "Pressure", "WindSpeed","WindMax","PrecipPast1h","Visibility","Weather"]


# Get temperature observations from DMI station in given time period
from collections import OrderedDict
all_dfs=[]
for param in parameters:
    allvals=[]
    alltimes=[]
    observations = client.get_observations(
        parameter=Parameter[param],
        station_id=dmi_station['properties']['stationId'],
        from_time=from_time,
        to_time=to_time,
        limit=200000)
    for obs in observations:
        value = obs["properties"]["value"]
        time = obs["properties"]["observed"]
        allvals.append(value)
        alltimes.append(time)
    df=pd.DataFrame({param:allvals,"date":alltimes})
    date1=datetime.strftime(from_time,"%Y%m%d")
    date2=datetime.strftime(to_time,"%Y%m%d")
    df.to_csv("_".join([param,date1,date2])+".csv",index=False)
    all_dfs.append(df)
sys.exit(0)

df1=all_dfs[0]
df2=all_dfs[4]

dif_list = [x for x in list(df1['date'].unique()) if x not in list(df2['date'].unique())]
#checking which ones missing values:
for df in all_dfs:
    print(f"{df.columns} {df.shape}")


#fill up the missing values
for date  in dif_list:
    df2 = df2.append(pd.Series([date,np.nan],index=["date","WindSpeed"]),ignore_index=True)
    #df2["Windspeed"]=df2["WindSpeed"].append(np.nan)

#for key in alldata.keys():
#    print(f"{key} {len(alldata[key])}")
#df=pd.DataFrame(alldata)
#df.to_csv("skagen_6months.csv",index=False)
