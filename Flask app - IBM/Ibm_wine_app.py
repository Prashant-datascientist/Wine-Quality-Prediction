# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 11:05:47 2022

@author: prash
"""
from flask import Flask, render_template, request
import requests
import os

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "-wNCRnnEIXbasWaTX3PE8-diVeixGrCGyZoDgz76NCkZ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app=Flask(__name__) # our flask app

@app.route('/') # rendering the html template
def home():
    return render_template('home.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")

@app.route('/data_predict', methods=['GET','POST']) # route for our prediction
def predict():
    input_feature=[float(x) for x in request.form.values() ]  
    #features_values=[np.array(input_feature)]

    payload_scoring = {"input_data":[{"fields":["type", "fixed_acidity","volatile_acidity",
                                                "citric_acid","residual_sugar","chlorides",
                                                "free_sulfur_dioxide","density","pH",
                                                "sulphates","alcohol"],"values":[input_feature]}]}


    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/358c4c65-f6f8-4008-8144-660032cc082e/predictions?version=2022-01-29', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    output = predictions['predictions'][0]['values'][0][0]
    print(output)
    #print(output)
     # predictions using the loaded model file
    #prediction=model.predict(x)  
    #print("Prediction is:",prediction)
     # showing the prediction results in a UI
    #prediction = (output)
    return render_template("pred.html",prediction=output)
if __name__=="__main__":
    
    # app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=False,use_reloader=False)
