import streamlit as st
import pandas as pd
import base64
#import matplotlib.pyplot as plt
#import matplotlib.dates as md
#from matplotlib.ticker import MaxNLocator
#import seaborn as sns
import numpy as np
#import yfinance as yf
#import sqlite3
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict

st.title('Wind speed prediction')

st.markdown("""
This app calculates the wind speed of a location in Greenland
based on a pre-trained model. \n
Data for the testing covers  period: 2021-11-06 14:20:00 to 2021-11-30 23:50:00
The user must select the date and time only inside this range
""")
min_date = datetime(2021,11,6)
max_date = datetime(2021,11,30)
#Load the data I used, then select only the testing part
df=pd.read_csv("weather_data/ikermit.csv.gz",compression='gzip')
df["date"] = [datetime.fromisoformat(dt[:-1]) for dt in df.date]
df.fillna(0,inplace=True)
df.sort_values(by=["date"],inplace=True)
#df = df[(df["date"] > min_date ) & (df["date"] < max_date)]

#Doing the splitting to select training data period
from sklearn.model_selection import train_test_split
df_train_full, df_test = train_test_split(df, test_size=0.2,random_state=4,shuffle=False)
df_train, df_val = train_test_split(df_train_full, test_size=0.25,random_state=42, shuffle=False)
# Data normalization
from sklearn.preprocessing import StandardScaler
feature_cols = ['WindSpeedPast1h', 'WindMax', 'WindGustAlwaysPast1h', 'WindMin', 'WindMinPast1h', 'TempDew', 'Pressure', 'PressureAtSea', 'WindDirPast1h', 'TempDry', 'Weather', 'TempMeanPast1h', 'TempMaxPast1h', 'TempMinPast1h', 'Humidity', 'HumidityPast1h', 'Visibility']
scaler = StandardScaler()
X_train= df_train[feature_cols]
scaler.fit(X_train)


# Read the sqlite file
def load_model(model_type="Linear regression"):
    model_file = { "Linear regression":"lin_reg.bin",
                   "Lasso regression": "lasso_reg.bin",
                   "Ridge regression": "ridge_reg.bin",
                   "Decision tree":"dec_tree"
                   }
    import pickle
    with open(model_file[model_type], 'rb') as f_in:
         model = pickle.load(f_in)
    return model

st.sidebar.header('User Input Parameters')



def user_input():
    """
    Select the date and return a dataframe with the data
    """
    selected_date = st.sidebar.date_input('date to predict', datetime(2021,11,6))

    select_model = st.sidebar.selectbox(
    "Select model",
    ("Linear regression", "Lasso regression", "Ridge regression","Decision tree")
)
    pred_date= datetime.combine(selected_date, datetime.min.time())
    if pred_date > max_date or pred_date < min_date:
        st.error(f"{pred_date} outside testing range!")
        #print(f"{pred_date} outside range!")

    #selet model
    model = load_model(select_model)
    #select only the value for this date:
    df_sel = df_test[df_test["date"] == pred_date]
    X_use= df_sel[feature_cols]
    X_use = scaler.transform(X_use)
    #y_pred = df_test["WindSpeed"].values


    #light = st.sidebar.slider('Lights use (Wh)', 0, 70, 10)
    #data["T_out"] = temp_out
    #data["RH_out"] = hum_out
    #for col in ['Press_mm_hg', 'Windspeed', 'Visibility', 'lights','Tdewpoint']:
    #    data[col] = 0.0
    #features = pd.DataFrame(data, index=[0])


    return X_use,df_sel,model
#df = user_input()
X_use,df_sel,model = user_input()
st.subheader('User Input parameters')
st.write(df_sel)
#lr = load_model()
prediction = model.predict(X_use)
#print(prediction[0])
st.subheader('Wind speed prediction (m/s)')
st.write(prediction[0])
#prediction = rf.predict(df)
#print(np.exp(prediction))
#st.write(np.exp(prediction[0]))


def calculate_prediction(data):
    '''
    Count days present for all days,
    starting at the beginning of each year
    Return a data frame with dates and number of days produced on each day
    '''
    return data_count
