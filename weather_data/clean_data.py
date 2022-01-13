"""
Read all the weather data downloaded with get_DMI_data.py 
and merge it in one file
"""
import pandas as pd
import os
import numpy as np
files=sorted(os.listdir("."))

mycolumns=["TempDry", "TempDew", "TempMeanPast1h", "TempMaxPast1h", "TempMinPast1h", "Humidity", "HumidityPast1h", "Pressure", "PressureAtSea", "WindDir", "WindDirPast1h", "WindSpeed", "WindSpeedPast1h", "WindGustAlwaysPast1h", "WindMax", "WindMinPast1h", "WindMin", "PrecipPast1h", "PrecipDurPast1h", "Visibility", "Weather", "LeavHumDurPast1h"]

period="_20200101_20211231"
if __name__=="__main__":
    #Use this variable as reference for the rest, since it is the one
    #that usually contains the longest record, every 10 min 
    var_ref = "TempDry"
    df_ref = pd.read_csv(var_ref+period+".csv")
    df_final= df_ref.copy() #make a copy of the original data
    for var in mycolumns:
        if var != var_ref:
            print(f"Merging {var} into data" )
            df_comp = pd.read_csv(var+period+".csv")
            df_final = df_final.merge(df_comp,how="left")
    #change the type of two of the columns to integer
    df_final["Weather"] = df_final["Weather"].astype("Int64")
    df_final["Visibility"] = df_final["Visibility"].astype("Int64")
    #dump the data to csv file
    df_final.to_csv("ikermit.csv",index=False)
