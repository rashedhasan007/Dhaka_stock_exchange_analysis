import numpy as np
#Relative Strength Index
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def COPP(df, n):  
    M = df['Close'].diff(int(n * 11 / 10) - 1)  
    N = df['Close'].shift(int(n * 11 / 10) - 1)  
    ROC1 = M / N  
    M = df['Close'].diff(int(n * 14 / 10) - 1)  
    N = df['Close'].shift(int(n * 14 / 10) - 1)  
    ROC2 = M / N
    roc=ROC1+ROC2
    Copp = pd.Series(roc.ewm(span = n, min_periods = n).mean(), name = 'Copp_' + str(n))    
    return (1000*Copp)

def coppcurve(df):
    fig = go.Figure([go.Candlestick(x=df.index,
                                   open=df['Open'], high=df['High'],
                                   low=df['Low'], close=df['Close']),go.Scatter(x=df.index, y=df['COPP'])])
    fig.update_layout(xaxis_rangeslider_visible=False, width=1200, height=500)

    return fig