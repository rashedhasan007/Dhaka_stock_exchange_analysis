from pmdarima import auto_arima
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#data = df.sort_index(ascending=True, axis=0)
def arima_training(train,valid):
    #train = data[:987]
    #valid = data[987:]

    training = train['Close']
    validation = valid['Close']

    model = auto_arima(training, start_p=1, start_q=1,max_p=3, max_q=3, m=12,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True)
    model.fit(training)

    forecast = model.predict(n_periods=1405)
    forecast = pd.DataFrame(forecast,index = valid.index,columns=['Prediction'])
    rms = np.sqrt(np.mean(np.power((np.array(valid['Close']) - np.array(forecast['Prediction'])), 2)))
    return forecast ,rms

def arima_plot(preds,new_data,valid,train):
    fig = plt.figure(figsize=(12, 8))
    valid['Predictions'] = 0
    valid['Predictions'] = preds

    valid.index = new_data[987:].index
    train.index = new_data[:1087].index

    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    return fig