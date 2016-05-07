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

def csv_extract_list(filename):
	'Extracts data from a csv and return as list of dictionaries\n\
	In this assignment it is used to get the train stops data from file'
	csv_list = list()

	# open csv file, strip encoding characters
	with io.open(filename, "r", encoding="utf-8-sig") as fo:

		# DictReader reads each csv line as a dictionary
		# with the header values as keys
		reader = csv.DictReader(fo)

		# append each dict to our stop list
		for row in reader:
			csv_list.append(row)

	# file is closed when 'with' ends

	return csv_list

### end of extract_csv_list() ###