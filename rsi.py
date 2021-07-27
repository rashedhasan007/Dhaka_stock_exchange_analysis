import numpy as np
#Relative Strength Index
import matplotlib.pyplot as plt
import plotly.graph_objects as go
def rsiFunc(prices, n=14):

    deltas = np.diff(prices)

    seed = deltas[:n+1]

    up = seed[seed>=0].sum()/n

    down = -seed[seed<0].sum()/n

    rs = up/down

    rsi = np.zeros_like(prices)

    rsi[:n] = 100. - 100./(1.+rs)



    for i in range(n, len(prices)):

        delta = deltas[i-1] # cause the diff is 1 shorter



        if delta>0:

            upval = delta

            downval = 0.

        else:

            upval = 0.

            downval = -delta



        up = (up*(n-1) + upval)/n

        down = (down*(n-1) + downval)/n



        rs = up/down

        rsi[i] = 100. - 100./(1.+rs)



    return rsi

def rsichart(title,df):
    fig = plt.figure(figsize=(20, 12))
    ax2 = plt.subplot2grid((10, 1), (5, 0), rowspan=4, colspan=1)
    ax2.plot(df, color='red', linewidth=2.5)
    ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
    ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
    ax2.set_title(title)
    return fig
def rsi_graph(df):
    fig = go.Figure([go.Scatter(x=df.index, y=df['RSI'])])
    fig.update_layout(xaxis_rangeslider_visible=False, width=1200, height=500)
    fig.add_hrect(y0=30, y1=30, line_width=5, fillcolor="red", opacity=1)
    fig.add_hrect(y0=70, y1=70, line_width=5, fillcolor="red", opacity=1)
    return fig

