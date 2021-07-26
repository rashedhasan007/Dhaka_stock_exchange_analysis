from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
def linear_reg(x_train,y_train,x_valid,y_valid):
    model = LinearRegression()
    model.fit(x_train,y_train)
    # make predictions and find the rmse
    preds = model.predict(x_valid)
    rms = np.sqrt(np.mean(np.power((np.array(y_valid) - np.array(preds)), 2)))
    return preds,rms

def L_plot(preds,new_data,valid,train):
    fig = plt.figure(figsize=(12,8))
    valid['Predictions'] = 0
    valid['Predictions'] = preds

    valid.index = new_data[987:].index
    train.index = new_data[:1087].index

    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    return fig