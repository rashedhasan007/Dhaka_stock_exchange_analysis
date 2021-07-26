#importing libraries
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

def K_training(x_train,y_train,x_valid,y_valid):
    #scaling data
    x_train_scaled = scaler.fit_transform(x_train)
    x_train = pd.DataFrame(x_train_scaled)
    x_valid_scaled = scaler.fit_transform(x_valid)
    x_valid = pd.DataFrame(x_valid_scaled)

    #using gridsearch to find the best parameter
    params = {'n_neighbors':[2,3,4,5,6,7,8,9]}
    knn = neighbors.KNeighborsRegressor()
    model = GridSearchCV(knn, params, cv=5)

    #fit the model and make predictions
    model.fit(x_train,y_train)
    preds = model.predict(x_valid)
    preds=pd.DataFrame(preds)
    rms = np.sqrt(np.mean(np.power((np.array(y_valid) - np.array(preds)), 2)))

    return preds,rms
def K_plot(preds,new_data,valid,train):
    fig = plt.figure(figsize=(12,8))
    valid['Predictions'] = 0
    valid['Predictions'] = preds

    valid.index = new_data[987:].index
    train.index = new_data[:1087].index

    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    return fig
