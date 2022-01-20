# 3rd  project for Alex Grigoriev's ML Zoomcamp

Since I missed the capstone project I am submitting this
project to finalize the bootcamp with at least 2 out of 3 
projects completed.

This project attempts to use ML to model the weather
in a location in Greenland.
The location was chosen as it is known to experience
extreme weather.
The main parameter to predict is wind speed.

The project was developed under Linux.

## Project description

Wind prediction in East Greenland

The data set consists of 10min and 1h data extracted at the synoptic station
Ikermit in Greenland (WMO code 04373). The data was extracted using the Danish 
Meteorological Institute's (DMI) [API](https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111).
The following variables were extracted for the last 2 yers (2020-01-01 to 2021-12-31)
- TempDry
- TempDew
- TempMeanPast1h
- TempMaxPast1h
- TempMinPast1h
- Humidity
- HumidityPast1h
- Pressure
- PressureAtSea
- WindDir
- WindDirPast1h
- WindSpeed
- WindSpeedPast1h
- WindGustAlwaysPast1h
- WindMax
- WindMinPast1h
- WindMin
- PrecipPast1h
- PrecipDurPast1h
- Visibility
- Weather
- LeavHumDurPast1h

Other variables, which should been available but came out empty were
- SnowDepthMan
- SnowCoverMan
- CloudCover
- CloudHeight
- RadiaGlob
- RadiaGlobPast1h
- SunLast1hGlob
- TempGrass
- TempSoil

The aim is to predict hourly wind speed using ML techniques.

## EDA and model development
The data was downloaded using the scripts provided in **weather_data**
- `get_DMI_data.py` gets the data
- ` clean_data.py` merges all the fields and outputs the data in one file.
The data was downloaded for 2 whole years (2020 and 2021)

The EDA and model selection is included in the jupyter notebok `data_eda.ipynb`.

The data was cleaned of missing values setting them to zero.
This turned out to be a sensitive issue, since there is many periods
without available data. Setting the data to zero in missing values
produces many sudden jumps and training the model for a long
period with the sudden jumps produces a very bad model in all cases.
Replacing the values with the means had the same effect.

The data split in test, validation and training was done without any reshuffling
in order to keep the order of the data stream.

Another issue was that selecting the whole period
led to memory issues in my laptop (ie, `not able to load 4.5 GB in memory`).
Hence in the end I only used data from Aug until Nov 2021 (there were
large patches missing in Dec 2021). This includes the data used
for training, validation and testing.
Since the model was trained for such a short period it
will not be very reliable predicting wind speeds outside
of this period.

Given the constraints is not surprise that a simple linear regression
worked quite well in this period. The final app (see below) is 
limited to only the testing period.

The final model is trained there and saved in a pickle file.

## Deployment

The requirements are included in Pipfile and Pipifile.lock
Use pipenv to activate environment with
`pipenv shell`

The app can be run in a container using the included
Dockerfile and the build.sh and rundocker.sh scripts.

The app can also be run using the stream1.py file 
included using streamlit as follows:
`streamlit run stream2.py`

It has also been deployed here



