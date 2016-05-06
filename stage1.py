#!/usr/bin/python

import sys
import os.path
from parsedt import parse_dt_str
from stops import csv_extract_list, validate_stop_name
from forecast import call_forecast_api, prettify_forcast

STOPS_FILE_PATH = "./google_transit/stops.txt"

# Validate usage
if len(sys.argv) < 2:
	print "Usage: " + sys.argv[0] + " < stop name > < date / time >"
	exit()

if not os.path.exists(STOPS_FILE_PATH):
	print "Error: Could not find stops file at path " + STOPS_FILE_PATH
	exit()

# Validate stop name
stops_list = csv_extract_list(STOPS_FILE_PATH)
stop_name = sys.argv[1]
stop_data = validate_stop_name(stop_name, stops_list)

if not stop_data:
	print "Error: Could not find stop with name " + stop_name
	exit()

# Validate and parse date / time
# No time given will return current time
date_time = parse_dt_str(" ".join(sys.argv[2:]))

forecast = call_forecast_api(stop_data["stop_lat"], stop_data["stop_lon"], date_time)

pretty_weather = prettify_forcast(forecast)

print "location: " + stop_data['stop_name']
print "time: " + date_time

for key, value in pretty_weather.iteritems():
	print key + " - " + value