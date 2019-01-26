from keras.models import Sequential
from keras.layers import Dense

# define model
model = Sequential()
model.add(Dense(64, input_dim=128, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid')

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
