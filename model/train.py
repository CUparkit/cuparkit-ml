import numpy as np
import pandas as pd
import keras
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint 
from sklearn.model_selection import train_test_split
from models import build_lstm, build_mlp

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

# generate input sequences of len = time_lag
time_lag = 24
step_size = 6
n_steps = int((X.shape[0]/step_size)-time_lag-1)
X_seq = []
y_seq = []
for i in range(n_steps):
	X_seq.append(X[i*step_size:(i*step_size+time_lag)])
	y_seq.append(y[i*step_size+time_lag])

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)	

# train test split
X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.10, random_state=42)

print("X train shape: {}".format(X_train.shape))
print("Y train shape: {}".format(y_train.shape))
print("X test shape: {}".format(X_test.shape))
print("Y test shape: {}".format(y_test.shape))

model = build_lstm(X.shape[1], time_lag)
#model = build_mlp(X_train.shape[1])

# checkpoint
filepath = "model/trained/{epoch:02d}-{loss:.6f}-{val_loss:.6f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(X_train, y_train, 
		validation_data=(X_test,y_test),
		callbacks=callbacks_list,
		epochs=150, 
		batch_size=10)
	
