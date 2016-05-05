#!/usr/bin/python

import io
import csv
import re

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

def validate_stop_name(name, stop_list):

	matched_stops_list = list()

	pattern = re.escape(name)

	for stop in stop_list:
		mo = re.search(pattern, stop["stop_name"], re.I)

		if mo:
			matched_stops_list.append(stop)


	return matched_stops_list

### end of validate_stop_name() ###