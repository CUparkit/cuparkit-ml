import numpy as np
import pandas as pd
import keras

# set random seed for reproducability
np.random.seed(42)

# load parking data
lot1 = pd.read_csv("datasets/santa_monica_parking/lot_1_north_hourly.csv")

model.fit(X, Y, epochs=150, batch_size=10)