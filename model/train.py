import numpy as np
import pandas as pd
import pyrebase
import keras
import sys
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint 
from sklearn.model_selection import train_test_split
from models import build_lstm, build_mlp

# set random seed for reproducability
np.random.seed(42)

# train type
train_type = 'online' # local - use csv file | online - use database

# load parking data
if train_type == 'local':
	parking = pd.read_csv('datasets/santa_monica_parking/parking_lot_counts_hourly.csv')
	parking = parking.sort_values(by='Datetime')

	lot_data_sequences = {}

	for lot_id in range(0, 18):
		# get data values for a single lot
		lot_df = parking.loc[parking['Lot id'] == lot_id]
	
		# extract features
		month_list = to_categorical(list(lot_df['Month']), num_classes=12)
		day_list = to_categorical(lot_df['Day'], num_classes=7)
		hour_list = to_categorical(lot_df['Time'], num_classes=24)
		lot_list = to_categorical(lot_df['Lot id'], num_classes=18)
		avail_list = lot_df['Percent Available']

		input_feature_vectors = []
		# create feature vectors
		for month, day, hour, lot in zip(month_list, day_list, hour_list, lot_list):				
			feature_vector = np.concatenate((month, day, hour, lot))
			input_feature_vectors.append(feature_vector)
			lot_data_sequences[lot_id] = {'feature_vectors': input_feature_vectors, 
											'availability': avail_list}

elif train_type == 'online':
	# Set up firebase database
	config = {
	"apiKey": "AIzaSyCBFSZ-DGVAEJHWO0iGkQRzQSZPwUXmLd4",
	"authDomain": "cuparkit.firebaseapp.com",
	"databaseURL": "https://cuparkit.firebaseio.com/",
	"storageBucket": "cuparkit.appspot.com",
	"serviceAccount": "cuparkit-firebase-adminsdk-l1n4y-e6336850e9.json"
	}

	firebase = pyrebase.initialize_app(config)
	db = firebase.database()

	lot_data_sequences = {}
	for lot_id in range(0, 18):

		surveys = db.child('surveys').child('lots').child(lot_id).get()
		lot_df = pd.DataFrame(surveys.val())
		lot_df = lot_df.sort_values(by='timestamp')

		month_list = []
		day_list = []
		hour_list = []
		lot_list = []

		for idx, val in lot_df.iterrows():
			
			dt = pd.to_datetime(val['timestamp'])

			month_list.append(dt.month)
			day_list.append(dt.weekday())
			hour_list.append(dt.hour)
			lot_list.append(lot_id)


		month_list = to_categorical(month_list, num_classes=12)
		day_list = to_categorical(day_list, num_classes=7)
		hour_list = to_categorical(hour_list, num_classes=24)
		lot_list = to_categorical(lot_list, num_classes=18)
		avail_list = lot_df['percentFull']

		input_feature_vectors = []
		# create feature vectors
		for month, day, hour, lot in zip(month_list, day_list, hour_list, lot_list):				
			feature_vector = np.concatenate((month, day, hour, lot))
			input_feature_vectors.append(feature_vector)
			lot_data_sequences[lot_id] = {'feature_vectors': input_feature_vectors, 
											'availability': avail_list}

# checkpoint
filepath = "model/test_trained/{epoch:02d}-{loss:.6f}-{val_loss:.6f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model = None

for epoch in range(5):
	for lot_id, val in lot_data_sequences.items():
		
		print("Training on lot id {}".format(lot_id))

		X = np.array(val['feature_vectors'])
		y = np.array(val['availability'])

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

		#print("X train shape: {}".format(X_train.shape))
		#print("Y train shape: {}".format(y_train.shape))
		#print("X test shape: {}".format(X_test.shape))
		#print("Y test shape: {}".format(y_test.shape))

		if not model:
			model = build_lstm(X.shape[1], time_lag)

		model.fit(X_train, y_train, 
				validation_data=(X_test,y_test),
				callbacks=callbacks_list,
				epochs=1, 
				batch_size=10)

model.save('final-lstm.hdf5')
