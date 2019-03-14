from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.template import Context, loader
from joblib import load
import pandas as pd

def regression_model(model_year, horsepower, weight, accel, displacement, origin, cylinders):
    #Import Scalers
    regressor = load(r"C:\Users\Jacinto D'Souza\Documents\Waterloo\Management Engineering\3A\MSCI 436 - Decision Support Systems\Project\MPG_Predictor\\regressor.joblib")
    scaler = load(r"C:\Users\Jacinto D'Souza\Documents\Waterloo\Management Engineering\3A\MSCI 436 - Decision Support Systems\Project\MPG_Predictor\\scaler.joblib")
    mpg_data = pd.DataFrame([cylinders, displacement, horsepower, weight, accel, model_year, origin])
    mpg_data = mpg_data.transpose()
    mpg_data = scaler.transform(mpg_data)
    predicted_value = regressor.predict(mpg_data)
    return(predicted_value)

def index(request):
    return render(request, "mpg/index.html")


def prediction(request):
    if request.method == "POST":
        car_name = request.POST['car_name']
        model_year = request.POST['model_year']
        horsepower = request.POST['horsepower']
        weight = request.POST['weight']
        accel = request.POST['accel']
        displacement = request.POST['displacement']
        origin = request.POST['origin']
        cylinders = request.POST['cylinders']

        predicted_value = regression_model(model_year, horsepower, weight, accel, displacement, origin, cylinders)

        return HttpResponse(predicted_value)
