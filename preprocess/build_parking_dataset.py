import os
import sys
import glob
import datetime
import numpy as np
import pandas as pd					
import urllib.request				# grab data from the web
from ish_parser import ish_report 	# easy way to parse through weird NOAA data
from collections import OrderedDict

SANTA_MONICA_PARKING = 'https://data.smgov.net/api/views/ng8m-khuz/rows.csv?accessType=DOWNLOAD'
SANTA_MONICA_WEATHER = ['ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2014/722885-93197-2014.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2015.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2016.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2017.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2018.gz']

lot_details = {	'Beach House Lot': {'id' : 0,  'capacity' : 274},
			   	'Civic Center' :   {'id' : 1,  'capacity' : 882},
			   	'Library'      :   {'id' : 2,  'capacity' : 532},
				'Lot 1 North'  :   {'id' : 3,  'capacity' : 1217},
				'Lot 3 North'  :   {'id' : 4,  'capacity' : 492},
				'Lot 4 South'  :   {'id' : 5,  'capacity' : 1496},
				'Lot 5 South'  :   {'id' : 6,  'capacity' : 885},
				'Lot 8 North'  :   {'id' : 7,  'capacity' : 217},
				'Pier Deck'    :   {'id' : 8,  'capacity' : 280},
				'Structure 1'  :   {'id' : 9,  'capacity' : 365},
				'Structure 2'  :   {'id' : 10, 'capacity' : 654},
				'Structure 3'  :   {'id' : 11, 'capacity' : 500},
				'Structure 4'  :   {'id' : 11, 'capacity' : 698},
				'Structure 5'  :   {'id' : 11, 'capacity' : 671},
				'Structure 6'  :   {'id' : 11, 'capacity' : 747},
				'Structure 7'  :   {'id' : 11, 'capacity' : 820},
				'Structure 8'  :   {'id' : 11, 'capacity' : 1370},
				'Structure 9'  :   {'id' : 11, 'capacity' : 298}}

def download_datasets():
	if not os.path.isdir('datasets'):
		os.makedirs('datasets')

		# get Santa Monica parking data
		urllib.request.urlretrieve(SANTA_MONICA_PARKING, 'datasets/santa_monica_parking/Parking_Lot_Counts.csv')

		# get hourly NOAA weather for 2014-2017
		for year_url in SANTA_MONICA_WEATHER:
			year_url.split('/')
			#urllib.request.urlretrieve(year_url, 'datasets/santa_monica_parking/Parking_Lot_Counts.csv')

def create_hourly_lot_datasets():

	print("Loading Santa Monica Parking dataset...")
	park_df = pd.read_csv("datasets/santa_monica_parking/Parking_Lot_Counts_subset.csv")

	hourly_rows = []
	print("Parsing dates and times...")
	for idx, row in park_df.iterrows():
		date_and_time = row['Date/Time']
		date = date_and_time.split()[0]

		if int(date_and_time.split()[1].split(':')[1]) != 0:
			continue

		hr = int(date_and_time.split()[1].split(':')[0])
		mn = int(date_and_time.split()[1].split(':')[1])

		if date_and_time.split()[2] == 'PM' and hr != 12:
			hr += 12 # convert to military time

		time = "{}".format(hr)

		month = int(date.split('/')[0])
		day = int(date.split('/')[1])
		year = int(date.split('/')[2])

		date_obj = datetime.datetime(year, month, day, hr, mn, 0)
		print(date_obj)

		day_of_week = date_obj.weekday()

		#if row['Available']/lot_details[row['Lot']]['capacity'] > 1.0:
		#	print(row['Lot'])

		row_dict = OrderedDict({'Date': date, 'Month': month, 'Day': day_of_week, 'Time': time, 
								'Lot id': lot_details[row['Lot']]['id'] , 'Lot name': row['Lot'], 
								'Available': row['Available'], 'Percent Available': row['Available']/lot_details[row['Lot']]['capacity']}) 

		hourly_rows.append(row_dict)
		if idx % 10 == 0:
			sys.stdout.write("* {}/{}\r".format(idx, '10000'))
			sys.stdout.flush()

	print("Creating new dataframe...")
	hourly_df = pd.DataFrame(hourly_rows)
	hourly_df.to_csv('datasets/santa_monica_parking/parking_lot_counts_hourly.csv')

	#df1['e'] = Series(np.random.randn(sLength), index=df1.index)
	#park_df.set_index('Lot')
	#park_df.loc['Lot 1 North'].to_csv('datasets/santa_monica_parking/lot_1_north_hourly.csv')

	#park_df.loc[(park_df['Lot'] == 'Lot 1 North') & (park_df['Date/Time'].isin(VALID_TIMES))].to_csv('datasets/santa_monica_parking/lot_1_north_hourly.csv')

def create_hourly_weather_datasets():

	for year in glob.glob('datasets/santa_monica_weather/*'):
		lines = [line.rstrip('\n') for line in open(year)]
		hourly_rows = []
		for line in lines:
			rpt = ish_report().loads(line)
			#row_dict = {'Date'}
			print(rpt.datetime)


if __name__ == '__main__':
	#download_datasets()
	create_hourly_lot_datasets()
	create_hourly_weather_datasets()


