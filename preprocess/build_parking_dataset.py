import os
import numpy as np
import pandas as pd					
import urllib.request				# grab data from the web
from ish_parser import ish_report 	# easy way to parse through weird NOAA data

SANTA_MONICA_PARKING = 'https://data.smgov.net/api/views/ng8m-khuz/rows.csv?accessType=DOWNLOAD'
SANTA_MONICA_WEATHER = ['ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2014/722885-93197-2014.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2015.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2016.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2017.gz',
						'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2015/722885-93197-2018.gz']

if not os.path.isdir('datasets'):
	os.makedirs('datasets')

	# get Santa Monica parking data
	urllib.request.urlretrieve(SANTA_MONICA_PARKING, 'datasets/santa_monica_parking/Parking_Lot_Counts.csv')

	# get hourly NOAA weather for 2014-2017
	for year_url in SANTA_MONICA_WEATHER:
		year_url.split('/')
		#urllib.request.urlretrieve(year_url, 'datasets/santa_monica_parking/Parking_Lot_Counts.csv')

print("Loading Santa Monica Parking dataset...")
park_df = pd.read_csv("datasets/santa_monica_parking/Parking_Lot_Counts.csv")

park_df.set_index('Lot', inplace=True)
print(park_df.loc['Lot 1 North'])
