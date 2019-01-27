import keras
import pyrebase
import datetime
import numpy as np
from keras.models import load_model
from keras.utils import to_categorical

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

# Read in the predicitions from the past day
print('Getting past predicitions from database...')
y_old = np.random.rand(24)

# load the trained model 
model = load_model('model/trained/05-0.019137-0.019336.hdf5')

# get yesterday's date
old_dt = datetime.datetime.now() - datetime.timedelta(days=1)
old_month = to_categorical(old_dt.month, num_classes=12)
old_day = to_categorical(old_dt.weekday(), num_classes=7)

# get the current date
dt = datetime.datetime.now()
month = to_categorical(dt.month, num_classes=12)
day = to_categorical(dt.weekday(), num_classes=7)

hours = np.arange(0, 24)
lots = np.arange(0, 18)

print("Generating feature vectors and predictions for each lot")
for lot in lots:
	old_vecs = []
	new_vecs = []
	lot = to_categorical(lot, num_classes=18)
	for hour in hours:
		hour = to_categorical(hour, num_classes=24)
		new_vecs.append(np.concatenate((month, day, hour, lot)))
		old_vecs.append(np.concatenate((old_month, old_day, hour, lot)))
	X = np.array(old_vecs + new_vecs)


	# generate input sequences of len = time_lag
	time_lag = 24
	step_size = 1
	n_steps = 24
	X_seq = []

	for i in range(n_steps):
		X_seq.append(X[i+1:(i+1+time_lag)])

	X_seq = np.array(X_seq)
	preds = model.predict(X_seq)
	print(preds.flatten())
