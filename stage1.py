#!/usr/bin/python

import sys
import os.path
from parsedt import parse_dt_str
from stops import csv_extract_list, validate_stop_name
from forecast import call_forecast_api, prettify_forcast

# Path to the stops file
STOPS_FILE_PATH = "stops.txt"

# Validate usage
if len(sys.argv) < 2:
	print "Usage: " + sys.argv[0] + " < stop name > < date / time >"
	exit()

# Validate stops file exists
if not os.path.exists(STOPS_FILE_PATH):
	print "Error: Could not find stops file at path " + STOPS_FILE_PATH
	exit()

# Stop name is always the first arg
stop_name = sys.argv[1]
# Everything after is datetime
dt_select_string = " ".join(sys.argv[2:])

# List of stops is in a file, so get the list from it
stops_list = csv_extract_list(STOPS_FILE_PATH)
# Validate the users input against the list of stops
valid_stops = validate_stop_name(stop_name, stops_list)

date_time = parse_dt_str(dt_select_string)

# Users input may have matched one, multiple or no stops
if len(valid_stops) < 1:
	print "No match for stop name: " + stop_name
	exit()
# If it matches multiple stops then get the user to pick one
elif len(valid_stops) > 1:
	print "Ambiguous stop name, which did you mean?"

	for index, stop in enumerate(valid_stops):
		print "[" + str(index) + "] " + stop["stop_name"]

	response = int(raw_input(": "))

	if response >= 0 and response < len(valid_stops):
		valid_stop = valid_stops[response]
	else:
		print "You are beautiful but your input was wrong."
		exit()
# Just one match so select it
else:
	valid_stop = valid_stops[0]

# Call the forecast api
forecast = call_forecast_api(valid_stop["stop_lat"], valid_stop["stop_lon"], date_time)

pretty_weather = prettify_forcast(forecast)

print "location: " + valid_stop['stop_name']
print "time: " + date_time
for key, value in pretty_weather.iteritems():
	print key + " - " + value