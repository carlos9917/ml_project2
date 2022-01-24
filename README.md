# 3rd  project for Alex Grigorev's ML Zoomcamp

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
The data was downloaded using the scripts provided in the directory `weather_data``
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
In the end I was forced to use only a continuous series of data
(from Aug until Dec 2021). 

The data is split in test, validation and training was done without any reshuffling
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

The final models are trained in the jupyter notebook and saved in pickle files.

The following models were tested:
- Linear regression
- Lasso regression
- Ridge regression
- Decision tree
- Recurrent neural network (Sequential)

The models that performed best were the linear and Lasso models.
The RNN model performed quite poorly, but this is probably
due to the large amount of features I used (16). It would 
make more sense to get rid of some of these (not tested for lack of time).
I tried this, but also got very poor results. I include the model here
for reference only, since I do not use it in the predictions.

## Deployment
The environment has been encapsulated using `pipenv`.
The requirements are included in Pipfile and Pipifile.lock
Use pipenv to activate environment with
`pipenv shell`

### test prediction
To test the prediction run:
`python predict.py`
and in another terminal run:
`python predict-test.py`

The prediction can be based on providing date or asking for data
from DMI's API (**note you need to setup your own API key for this to work**):

Change the date in `predict-test.py` to try a different date or select new data.
When setting `request-weather-data`to False only the test period can be used:
(2021-11-6 to 2021-11-30)

```
wind_res = {"date": "2021-11-07",
             "request-weather-data": False
            }

```

### containerization
The prediction can be run in a container using the included scripts:

- Dockerfile  
- build.sh  
- run_container.sh scripts

Build the image using `build.sh`
Run a container using `run_container.sh`

To run the prediction use:
`python predict.py`
This will run the Flask server.
Then in another terminal run
`python predict-test`

and this should print the predictions from the different models
for the given date. To call the DMI API from inside the container
you will need to include the `DMI_API_KEY` in the Dockerfile
or hard code it in the `get_weather_features.py` script.


### Web deployment

The prediction can also be tested using the `stream2.py` file 
included using streamlit as follows:
`streamlit run stream2.py`
### NOTE: 
you need to install streamlit locally first using
pipenv install streamlit
Installing it and adding it to my Pipfile caused
some library clashes in my app deployment to streamlit.

The app has been deployed [here](https://share.streamlit.io/carlos9917/ml_project2)

NOTE: This app will only work providing a given date that falls inside the testing period.
