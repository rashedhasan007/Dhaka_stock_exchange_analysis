import investpy
import pandas as pd
import plotly.graph_objects as go

def livechart(df):
    fig=go.Figure(data=[go.Candlestick(x=df.index,
                                   open=df['Open'], high=df['High'],
                                   low=df['Low'], close=df['Close'])
                    ])

    fig.update_layout(xaxis_rangeslider_visible=False, width=1200, height=500)

    return fig