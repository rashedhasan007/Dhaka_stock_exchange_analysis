#create features
from fastai.tabular import add_datepart
import pandas as pd
def refine(df):
    x = len(df) - 1
    num_index = range(0, x, 1)
    df = df.reset_index()
    # df = df.set_index(num_index)
    df = pd.DataFrame(df)
    print(df)
    # setting index as date values
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
    df.index = df['Date']

    # sorting
    data = df.sort_index(ascending=True, axis=0)

    # creating a separate dataset
    new_data = pd.DataFrame(index=range(0, len(df)), columns=['Date', 'Close'])

    for i in range(0, len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]

    add_datepart(new_data, 'Date')
    new_data.drop('Elapsed', axis=1, inplace=True)  # elapsed will be the time stamp

    new_data['mon_fri'] = 0
    for i in range(0, len(new_data)):
        if (new_data['Dayofweek'][i] == 0 or new_data['Dayofweek'][i] == 4):
            new_data['mon_fri'][i] = 1
        else:
            new_data['mon_fri'][i] = 0

    # split into train and validation
    train = new_data[:1087]
    valid = new_data[987:]
    print(valid)

    x_train = train.drop('Close', axis=1)
    y_train = train['Close']
    x_valid = valid.drop('Close', axis=1)
    y_valid = valid['Close']
    return x_train,y_train,x_valid,y_valid,new_data,valid,train