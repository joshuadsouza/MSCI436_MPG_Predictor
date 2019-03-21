#Import modules
import pymysql
import pandas as pd
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from joblib import dump
from pathlib import Path
from dotenv import load_dotenv
import os
env_path = Path('./mpg_pred/mpg_pred') / '.env'
load_dotenv(dotenv_path=env_path)

#Model
model = GradientBoostingRegressor()


#Get the column headers
def get_headers(columns):
    column = []
    columns = list(columns)
    for item in columns:
        column.append(item[0])
    return column


#Connect to database and retrieve results
connection = pymysql.connect(host=os.getenv("HOST"),
                            user=os.getenv("USER"),
                            password=os.getenv("PASSWORD"),
                            db=os.getenv("DB"))

#Get Results from the Database
with connection.cursor() as cursor:
    #Get results
    sql = "select * from MPGDATA"
    cursor.execute(sql)
    columns = cursor.description
    columns = get_headers(columns)
    results = cursor.fetchall()

#Close connection
connection.close()

#Convert Results into Database
results = pd.DataFrame(list(results), columns=columns)

#Drop columns not needed
results = results.drop(["MpgID", "VehicleName"], axis=1)
columns.remove("MpgID")
columns.remove("VehicleName")

#Scale the Data
results = pd.DataFrame(results, columns=columns)

Y = pd.DataFrame(results['MPG'])

X = results.drop("MPG", axis=1)

scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

seed = 7
kfold = model_selection.KFold(n_splits=15, random_state=seed)

#Negative Mean Squared Error
scoring = "neg_mean_squared_error"
model_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
print(model_results.mean())


#from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=.20)
#model.fit(X_train, y_train)
#y_pred = model.predict(X_test)

#Train Regressor
gradientRegressor = GradientBoostingRegressor()
gradientRegressor.fit(X, Y)

#Export Gradient Regressor and scaler
dump(gradientRegressor, 'regressor.joblib')
dump(scaler, 'scaler.joblib')