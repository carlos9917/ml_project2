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


Two random variables were also included in the data set for testing the regression models and to filter out non predictive attributes (parameters). Not sure what the hell this means, haven't read the paper!


## EDA and model development
The EDA and model selection is included in the attached 
jupyter notebok
`data_eda.ipynb` for details.
Final model is trained there and saved in a pickle file.

## Deployment

The requirements are included in Pipfile and Pipifile.lock
Use pipenv to activate environment with
pipenv shell

The code can be run in a container using the included
Dockerfile and the build.sh and rundocker.sh scripts.

