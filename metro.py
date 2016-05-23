#!/usr/bin/python

import io
import csv
import re

STOPS_FILE_PATH = "./google_transit/stops.txt"

class metro_data():
	"""

	This class hold the metro train stops data 
	that is pulled from file.

	It includes two helper functions used for
	displaying the data.

	"""

	def __init__(self):
		self.stop_list = csv_extract_list(STOPS_FILE_PATH)

	def find_stop(self, name):
		pattern = re.escape(name)

		for stop in self.stop_list:
			mo = re.match(pattern, stop["stop_name"], re.I)

			if mo:
				return stop


	def getTidyNameList(self):
		pattern = r'^([\w\s\-\(\)]*) Railway.*'

		nameList = list()

		for stop in self.stop_list:
			mo = re.match(pattern, stop["stop_name"], re.I)

			if mo:
				nameList.append(mo.group(1))
			else:
				nameList.append(stop["stop_name"])
				print stop["stop_name"]

		return nameList


## end of class metro_data ###

def csv_extract_list(filename):
	"""

	Extracts data from a csv and return as list of dictionaries
	In this assignment it is used to get the train stops data from file


	"""
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