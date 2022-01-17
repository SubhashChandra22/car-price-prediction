from flask import Flask, render_template, request
from flask import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app=Flask(__name__)
model=pickle.load(open('random_forest_regression_model.pkl','rb'))

@app.route("/predict",methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    Year=int(request.json['Year'])
    Present_price=float(request.json['Present_Price'])
    Kms_Driven=int(request.json['Kms_Driven'])
    Kms_Driven2=np.log(Kms_Driven)
    Owner=int(request.json['Owner'])
    Fuel_Type_Petrol=request.json['Fuel_Type_Petrol']
    if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1
    Year=2020-Year
    Seller_Type_Individual=request.json['Seller_Type_Individual']
    if(Seller_Type_Individual=='Individual'):
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0
    Transmission_Mannual=request.json['Transmission_Mannual']
    if(Transmission_Mannual=='Mannual'):
        Transmission_Mannual=1
    else:
        Transmission_Mannual=0	

        
    prediction=model.predict([[Present_price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
    output=round(prediction[0],2)
    
    # if output<0:
    #     return jsonify({'prediction':"can't sell this car"})
    # else:
    print(output)
    if output<0:
        return jsonify ({"Prediction":"This car can't be sell out"})
    else:
        return jsonify({'The estimated price of care is':output*100000})

if __name__=="__main__":
   app.run(debug=True)
