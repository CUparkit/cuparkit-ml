from keras.models import Sequential
from keras.layers import Dense, LSTM

def build_mlp(input_dim):
    # define model
    model = Sequential()
    model.add(Dense(128, input_dim=input_dim, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='mean_squared_error', optimizer='adam')

    return model

def build_lstm(input_dim, time_lag):
    # define model
    model = Sequential()
    model.add(LSTM(64, input_shape=(time_lag, input_dim), return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='mean_squared_error', optimizer='adam')

    return model