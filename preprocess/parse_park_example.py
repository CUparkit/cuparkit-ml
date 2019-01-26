import pandas as pd

park_df = pd.read_csv("Parking_Lot_Counts.csv")

lots = []

for idx, row in park_df.iterrows():
	if row['Lot'] not in lots:
		lots.append(row['Lot'])
	print("row: {} | lots: {}".format(idx, len(lots)))

print(lots)
print('Found {} lots'.format(len(lots)))