# -*- coding: utf-8 -*-
"""regressionML.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13_O29cmFpzzeWIrFjOozHZESvGyKZGqy
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from  sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error,mean_squared_error

def mean_square_error(x, y):
    pred = 1
    error = np.mean((y-pred)**2)
    return error
def run_regression():
  p = np.loadtxt("SatelliteConjunctionDataRegression.csv", delimiter=",",skiprows=1)
  data = shuffle(p)
  Xset = data[:,0:-1]
  Yset = data[:,[-1]]

  print("_____________")

  scaler = StandardScaler()
  scalerY = StandardScaler()
  scalerYV = StandardScaler()
  scalerYTest = StandardScaler()

  Xtemp,Xtest, Ytemp, Ytest = train_test_split(Xset, Yset, train_size = 0.8)
  Xtrain, Xvalid,Ytrain,Yvalid = train_test_split(Xtemp, Ytemp, train_size = 0.75)

  #print(Xtrain.shape)

  #NOT SURE ABOUT FITING ALLA THE SCALERS

  Xtrain_Scaled = scaler.fit_transform(Xtrain)
  Ytrain_Scaled = scalerY.fit_transform(Ytrain.reshape(-1, 1))
  Xvalid_Scaled = scaler.transform(Xvalid)
  Yvalid_Scaled = scalerYV.fit_transform(Yvalid.reshape(-1, 1))
  Xtest_Scaled = scaler.transform(Xtest)

  Regr = LinearRegression()
  #RegrV = LinearRegression()



  plotX=range(1,7)
  plotY=[]
  plotYV=[]

  minerror = 1000000000
  bestRegr = LinearRegression()
  minOrder = 0
  fig, axs = plt.subplots(2, 6, figsize=(30, 10))
  for i in range(1,7):
    print(i)
    Poly = PolynomialFeatures(i, include_bias=False)
    #PolyV = PolynomialFeatures(i, include_bias=False)

    Xtrain_Poly = Poly.fit_transform(Xtrain_Scaled)
    Xvalid_Poly = Poly.transform(Xvalid_Scaled)

    #LEARN ON TRAIN DATA AND THE VALIDATE PREDICITON ON DATA WHICH IT DIDNT TRAIN 
    Regr.fit(Xtrain_Poly, Ytrain_Scaled)
    #RegrV.fit(Xvalid_Poly, Yvalid_Scaled) 
    
    predictionScaled=Regr.predict(Xtrain_Poly)
    predictionScaled_V=Regr.predict(Xvalid_Poly)

    prediction=scalerY.inverse_transform(predictionScaled)
    predictionV=scalerYV.inverse_transform(predictionScaled_V)
    
    print(predictionV.shape)

    #print(str(i)+str(":")+str(Regr.score(prediction, Ytest)))
    MSE,MSEV=0,0

    #RMS WAY OF CALCULATINGMSE
    MSE = np.sqrt(np.mean((Ytrain-prediction)**2))
    MSEV = np.sqrt(np.mean((Yvalid-predictionV)**2))

    print()
    #rmse=mean_squared_error(Ytrain,prediction)
    #rmseV=mean_squared_error(Yvalid,predictionV)
    plotY.append(MSE)
    plotYV.append(MSEV)

    print("MSE:"+str(MSE)+"\n")
    print("MSEvalidation:"+str(MSEV)+"\n")
    if(MSEV<minerror):
        #bestRegr = Regr
        minerror = MSEV
        minOrder = i
    maxx =min(max(max(prediction),max(predictionV)),max(max(Yvalid),max(Ytrain)))
    tempy = np.linspace(0,maxx, 1000)
    axs[0,i-1].plot(tempy, tempy, color="g")
    axs[0,i-1].set_title("Order "+str(i))
    axs[0,i-1].scatter(Ytrain, prediction)
    axs[0,i-1].scatter(Yvalid, predictionV)
    plt.xlabel("Actual value")
    plt.ylabel("Predicted value")
    maxy = max(max(Yvalid),max(Ytrain))
    miny = min(min(Yvalid),min(Ytrain))
    #plt.ylim(miny, maxy)
    axs[1,i-1].plot(tempy, tempy, color="g")
    axs[1,i-1].scatter(Ytrain, prediction)
    axs[1,i-1].scatter(Yvalid, predictionV)
    axs[1,i-1].set_title("Order "+str(i)+" zoom")
    plt.xlabel("Actual value")
    plt.ylabel("Predicted value")
    maxy = min(max(Yvalid),max(Ytrain))
    miny = max(min(Yvalid),min(Ytrain))
    plt.ylim(miny, maxy)
    
  plt.figure(21)
  plt.plot(plotX, plotY, color="r",label="train")
  plt.plot(plotX, plotYV, color="b",label="valid")

  #plt.plot(i, mses_training, label="Training set", color="blue")

  plt.xlabel("degree")
  plt.ylabel("MSE")
  plt.grid()
  plt.yscale("log")
  plt.show()


  print(minOrder)
  Poly = PolynomialFeatures(minOrder, include_bias=False)

  Xtrain_Poly = Poly.fit_transform(Xtrain_Scaled)
  Xtest_Poly = Poly.transform(Xtest_Scaled)
  bestRegr.fit(Xtrain_Poly, Ytrain_Scaled)

  predictionScaled_Test=bestRegr.predict(Xtest_Poly)
  prediction_Test=scalerY.inverse_transform(predictionScaled_Test)
  MSE_Test = np.sqrt(np.mean((Ytest-prediction_Test)**2))
  print(MSE_Test)