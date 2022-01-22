import pickle
from flask import Flask
from flask import request
from flask import jsonify
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
import pandas as pd

scaler = StandardScaler()
feature_cols = ['WindMax', 'WindGustAlwaysPast1h', 'WindMin', 'WindMinPast1h', 'TempDew', 'Pressure', 'PressureAtSea', 'WindDirPast1h', 'TempDry', 'Weather', 'TempMeanPast1h', 'TempMaxPast1h', 'TempMinPast1h', 'Humidity', 'HumidityPast1h', 'Visibility']

#the model can only be used to predict inside this testing period
min_date = datetime(2021,11,6)
max_date = datetime(2021,11,30)


def setup_models():
    """
    Load the pre-trained models.
    Also load the data. This is only to select the testing period
    which I will use later to select the date from
    
    """
    model_files = ["dec_tree.bin","lasso_reg.bin", "lin_reg.bin", "ridge_reg.bin"]
    
    models = {}
    for this_model in model_files:
        with open(this_model, 'rb') as f_in:
            model_name=this_model.replace(".bin","")
            models[model_name] = pickle.load(f_in)

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
        return None
    elif use_dmi_data:
        print("Please provide feature values for the following variables")
        print(feature_cols)
        print("NOT IMPLEMENTED YET!")
        sys.exit(1)
    else:
        df_test,models =  setup_models()
        df_sel = df_test[df_test["date"] == pred_date]
        X_use= df_sel[feature_cols]
        X_use = scaler.transform(X_use)
        return X_use,models

    

app = Flask('response')


@app.route('/predict', methods=['POST'])
def predict():
    pred_date = request.get_json()
    print(f"What I get from requests: {pred_date}")
    
    pred_date = datetime.strptime(pred_date["date"],"%Y-%m-%d")
    X_use, models = get_model_settings(pred_date)
    result={}
    for model in models.keys():
        y_pred = models[model].predict(X_use)
        #if model not in ["dec_tree","lasso_reg"]:
        #    print(y_pred[[0]])
        #print(f"Pred for {model}:{y_pred}")
        if model in ["dec_tree","lasso_reg"]:
            result[model] = y_pred[0]
        else:
            result[model] = y_pred[0][0]
    results = {"Wind speed predictions (m/s)": result}
    #result = {
    #    'Wind speed (m/s)': y_pred
    #}

    return jsonify(results)
    #return result


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=9999)

