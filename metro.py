#!/usr/bin/python

import io
import csv
import re

STOPS_FILE_PATH = "./google_transit/stops.txt"

class metro_data():

	def __init__(self):
		self.stop_list = csv_extract_list(STOPS_FILE_PATH)

	def find_stop(self, name):
		pattern = re.escape(name)

		for stop in self.stop_list:
			mo = re.match(pattern, stop["stop_name"], re.I)

			if mo:
				return stop

## end of class metro_data ###


# Extracts data from a csv and return as list of dictionaries
# In this assignment it is used to get the train stops data from file

def csv_extract_list(filename):

	csv_list = list()

	try:
		# open csv file, strip encoding characters
		with io.open(filename, "r", encoding="utf-8-sig") as fo:

			reader = csv.DictReader(fo)

			for row in reader:
				csv_list.append(row)

	except IOError:
		print "Fatal Error: " + filename + " not found!"
		exit()

	return csv_list

### end of extract_csv_list() ###