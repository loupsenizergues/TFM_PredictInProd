from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

PATH_TO_LOCAL_MODEL = 'model.joblib'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(pickup_datetime, pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count):
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

    # localize the datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
    result = {"key":"2013-07-06 17:18:00.000000119",
    "pickup_datetime": formatted_pickup_datetime,
    "pickup_longitude": float(pickup_longitude),
    "pickup_latitude": float(pickup_latitude),
    "dropoff_longitude": float(dropoff_longitude),
    "dropoff_latitude": float(dropoff_latitude),
    "passenger_count": int(passenger_count)}
    X = pd.DataFrame()
    for key,value in result.items():
        X[key]=[value]
    
    model = joblib.load(PATH_TO_LOCAL_MODEL)
    y_pred = model.predict(X)
    return {"fare": int(y_pred)}

"""def predict(pickup_datetime, pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count):
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

    # localize the datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
    result = {
    "pickup_datetime": [formatted_pickup_datetime],
    "pickup_longitude": [float(pickup_longitude)],
    "pickup_latitude": [float(pickup_latitude)],
    "dropoff_longitude": [float(dropoff_longitude)],
    "dropoff_latitude": [float(dropoff_latitude)],
    "passenger_count": [int(passenger_count)]}
    X = pd.DataFrame(data=result)
    X.insert(0,"key","2013-07-06 17:18:00.000000119")
    model = joblib.load(PATH_TO_LOCAL_MODEL)
    y_pred = model.predict(X)
    return {"fare": int(y_pred)}"""
        