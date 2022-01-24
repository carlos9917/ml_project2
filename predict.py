import pickle
from flask import Flask
from flask import request
from flask import jsonify
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
import pandas as pd
import sys
import numpy as np

scaler = StandardScaler()
feature_cols = ['WindMax', 'WindGustAlwaysPast1h', 'WindMin', 'WindMinPast1h', 'TempDew', 'Pressure', 'PressureAtSea', 'WindDirPast1h', 'TempDry', 'Weather', 'TempMeanPast1h', 'TempMaxPast1h', 'TempMinPast1h', 'Humidity', 'HumidityPast1h', 'Visibility']

#the model can only be used to predict inside this testing period
min_date = datetime(2021,11,6)
max_date = datetime(2021,11,30)

def split_sequence(sequence1, n_steps):
    """
    Function to split the data for the RNN model
    """
    X = list()
    for i in range(len(sequence1)):
    # find the end of this pattern
        print(i)
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence1)-1:
            break
        # gather input and output parts of the pattern
        #seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        seq_x = sequence1[i:end_ix]
        X.append(seq_x)
    return np.array(X)


def read_models():
    """
    Reads the pickle files and returns a dictionary with the models
    """
    model_files = ["dec_tree.bin","lasso_reg.bin", "lin_reg.bin", "ridge_reg.bin"] #,"rnn_model.bin"]
    models = {}
    for this_model in model_files:
        with open(this_model, 'rb') as f_in:
            model_name=this_model.replace(".bin","")
            models[model_name] = pickle.load(f_in)

    return models

def use_test_data():
    """
    Load the pre-trained models.
    Also load the original data. This is only to select the testing period
    which I will use later to select the date from
    
    """
    models = read_models()

    #Load the data I used, then select only the testing part
    df=pd.read_csv("weather_data/ikermit.csv.gz",compression='gzip')
    df["date"] = [datetime.fromisoformat(dt[:-1]) for dt in df.date]
    df.fillna(0,inplace=True)
    df.sort_values(by=["date"],inplace=True)
    #Doing the splitting to select training data period
    df_train_full, df_test = train_test_split(df, test_size=0.2,random_state=4,shuffle=False)
    df_train, df_val = train_test_split(df_train_full, test_size=0.25,random_state=42, shuffle=False)
    # Data normalization
    X_train= df_train[feature_cols]
    scaler.fit(X_train)
    return df_test, models

def get_model_settings(pred_date,use_dmi_data=False):
    """
    The model uses the values of the features
    included in the testing period, hence it will
    return None unless use_dmi_data is set to True
    """
    if pred_date > max_date or pred_date < min_date and not use_dmi_data:
        return None, None
    elif use_dmi_data:
        #print("Please provide feature values for the following variables")
        #print(feature_cols)
        models =  read_models()
        from get_weather_features import print_data
        features_weather = print_data(datetime.strftime(pred_date,"%Y-%m-%d"))
        df_sel = pd.DataFrame.from_dict(features_weather)
        X_use= df_sel[feature_cols]
        scaler.fit(X_use)
        X_use = scaler.transform(X_use)
        return X_use,models
        #print("NOT IMPLEMENTED YET!")
        #sys.exit(1)
    else:
        df_test,models =  use_test_data()
        df_sel = df_test[df_test["date"] == pred_date]
        X_use= df_sel[feature_cols]
        X_use = scaler.transform(X_use)
        return X_use,models

    

app = Flask('response')


@app.route('/predict', methods=['POST'])
def predict():
    pred_this = request.get_json()
    if pred_this["request-weather-data"]:
        print(">>>>> Requesting feature values from DMIs API <<<<")
        pred_date = datetime.strptime(pred_this["date"],"%Y-%m-%d")
        X_use, models = get_model_settings(pred_date,use_dmi_data=True)
    else:
        print(">>>>> Using the testing period with pre-trained models <<<<")
        pred_date = datetime.strptime(pred_this["date"],"%Y-%m-%d")
        print(f"What I get from requests: {pred_date}")
        X_use, models = get_model_settings(pred_date)
        if any(x is None for x in [X_use, models] ):
            print(f"Date {pred_date} not in the testing interval")
            results = {"Wind speed predictions (m/s)": f"{pred_date} not in the test interval!"}
            return jsonify(results)
    result={}
    for model in models.keys():
        y_pred = models[model].predict(X_use)
        #if model != "rnn_model":
        #else:
        #    print("Calling extra split for data")
        #    print(X_use.shape)
        #    X2= split_sequence(X_use, len(feature_cols))
        #    print(X2)
        #    sys.exit(0)

        if model in ["dec_tree","lasso_reg"]:
            result[model] = y_pred[0]
        else:
            result[model] = y_pred[0][0]
    results = {"Wind speed predictions (m/s)": result}

    return jsonify(results)


if __name__ == "__main__":
    #app.run(debug=True, host='localhost', port=9999)
    app.run(debug=True, host='0.0.0.0', port=9999)

