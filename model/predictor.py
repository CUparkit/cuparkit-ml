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

hours = np.arange(0, 23)
lots = np.arange(0, 17)

print("Generating feature vectors for each lot")
for lot in lots:
	lot = to_categorical(lot, num_classes=18)
	for hour in hours:
		hour = to_categorical(hour, num_classes=24)
		feature_vector = np.concatenate((month, day, hour, lot))
		feature_vectors.append(feature_vector)

# generate input sequences of len = time_lag
time_lag = 24
step_size = 1
n_steps = int((X.shape[0]/step_size)-time_lag-1)
X_seq = []
y_seq = []
for i in range(n_steps):
	X_seq.append(X[i+1*step_size:(i+1*step_size+time_lag)])


print("Generating predictions...")
X_seq = np.array(X_seq)
print(X_seq.shape)
preds = model.predict(X_seq)
#print(preds.flatten())
