import mysql.connector
from mysql.connector import Error
import numpy as np
import pandas as pd


def trainMPG():
    # START USING PANDAS&NUMPY TO LEARN FROM THE DATA
    # DETERMINE THE TEST TRAIN SPLIT FROM THE DATAFRAME
    df = pd.DataFrame(mpgRecords,
                      columns=['MPGID', 'MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight', 'Accelleration',
                               'ModelYear', 'Origin', 'CarName'])
    df = df.drop(('CarName', 'MPGID'), axis=1)  # carName, MPGID is useless to our analysis
    df = df.astype(float)
    X = df.drop('MPG', axis=1)
    y = df['MPG'].astype(int) # cast to int to stop complaints

    # split data into training and testing data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.20)

    # NEURAL NETWORK
    # normalize
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    # fit only to the training data for our set
    scaler.fit(X_train)

    # now apply any transformations to our data
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # begin to learn
    from sklearn.neural_network import MLPClassifier
    mlp = MLPClassifier(hidden_layer_sizes=(8, 8, 8), max_iter=10000)
    mlp.fit(X_train, y_train)

    # test the model
    predictions = mlp.predict(X_test)
    from sklearn.metrics import classification_report, confusion_matrix
    print(confusion_matrix(y_test, predictions))
    print(classification_report(y_test, predictions))

    # return mlp.predict()

def findMPG():
    # find the MPG for a given car

    # result answer to web
    return mlp.predict()  #return prediction to user


# TRY TO CONNECT TO DB
# https://pynative.com/python-mysql-database-connection/
# https://pynative.com/python-mysql-select-query-to-fetch-data/
try:
    # Connect to the database
    connection = mysql.connector.connect(host='',
                                         database='',
                                         user='',
                                         password='')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MYSQL database... MySQL Server version on ", db_Info)

        # cursor = connection.cursor()
        # cursor.execute("select database();")
        # record = cursor.fetchone()
        # print("Your connected to - ", record)

        sql_select_Query = "select * from mpgdata"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        mpgRecords = cursor.fetchall()

        print ("Total number of rows in mpgdata is - ", cursor.rowcount)
        print ("Printing each row's coloumn values")
        for row in mpgRecords:
            print("MPGID = ", row[0], )
            print("MPG = ", row[1], )
            print("Cylinders = ", row[2], )
            print("Displacement = ", row[3], )
            print("Horsepower = ", row[4], )
            print("Weight = ", row[5], )
            print("Accelleration = ", row[6], )
            print("ModelYear = ", row[7], )
            print("Origin = ", row[8], )
            print("CarName = ", row[9], "\n")
        cursor.close()

        print(trainMPG())


except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    #Closing DB Connection
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        # with connection.cursor() as cursor: