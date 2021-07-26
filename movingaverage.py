import numpy as np
#Relative Strength Index
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Ease of Movement  
def EOM(df, n):  
    EoM = (df['High'].diff(1) + df['Low'].diff(1)) * (df['High'] - df['Low']) / (2 * df['Volume'])
    Eom_ma = pd.Series(EoM.rolling(n).mean(), name = 'EoM')
    df = df.join(10*Eom_ma)  
    return df

def movingcurve(df,n):
    name='EoM_'
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Candlestick(x=df.index,
                                   open=df['Open'], high=df['High'],
                                   low=df['Low'], close=df['Close']),row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['EoM']),
        row=2, col=1
    )
    fig.update_layout(xaxis_rangeslider_visible=False, width=1200, height=500)

    return fig