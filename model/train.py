import numpy as np
import pandas as pd
import keras
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from models import build_lstm, build_mlp

# convert an array of values into a dataset of sequences
def create_sequences(dataset, time_lag=1):
	X, Y = [], []
	for i in range(len(dataset)-time_lag-1):
		a = dataset[i:(i+time_lag), 0]
		X.append(a)
		Y.append(dataset[i + time_lag, 0])
	return numpy.array(X), numpy.array(Y)

# set random seed for reproducability
np.random.seed(42)

# load parking data
parking = pd.read_csv('datasets/santa_monica_parking/parking_lot_counts_hourly.csv')

# features
month_list = to_categorical(list(parking['Month']))
day_list = to_categorical(parking['Day'])
hour_list = to_categorical(parking['Time'])
lot_list = to_categorical(parking['Lot id'])
#temp_list = np.array(parking['Air temperature'])
#prec_list = np.array(parking['Preciptation'])
avail_list = parking['Percent Available']

# scale continuous features from [0,1]
#temp_list = (temp_list-np.min(temp_list))/(np.max(temp_list)-np.min(temp_list))
#prec_list = (prec_list-np.min(prec_list))/(np.max(prec_list)-np.min(prec_list))

input_feature_vectors = []
# create feature vectors
for month, day, hour, lot in zip(month_list, day_list, hour_list, lot_list):
							
	feature_vector = np.concatenate((month, day, hour, lot))
	input_feature_vectors.append(feature_vector)

X = np.array(input_feature_vectors)
y = np.array(avail_list)

time_lag = 5

X_seq = []
y_seq = []
for i in range(X.shape[0]-time_lag-1):
	X_seq.append(X[i:(i+time_lag)])
	y_seq.append(y[i+time_lag])

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)	

print("X seq shape: {}".format(X_seq.shape))
print("Y seq shape: {}".format(y_seq.shape))

# train test split
X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.10, random_state=42)

print("X train shape: {}".format(X_train.shape))
print("Y train shape: {}".format(y_train.shape))

model = build_lstm(X.shape[1], time_lag)
#model = build_mlp(X_train.shape[1])

model.fit(X_train, y_train, 
		validation_data=(X_test,y_test),
		epochs=150, 
		batch_size=10)