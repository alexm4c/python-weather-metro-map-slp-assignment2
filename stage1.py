#!/usr/bin/python

import sys
from metro import metro_data
from parsedt import parse_dt_str
from forecast import call_forecast_api, prettify_forcast

# Validate usage
if len(sys.argv) < 2:
	print "Usage: " + sys.argv[0] + " < stop name > < date / time >"
	exit()

# Validate stop name
stop_name = sys.argv[1]
stop_data = metro_data().find_stop(stop_name)

if not stop_data:
	print "Error: Could not find stop with name " + stop_name
	exit()

# Validate and parse date / time
# No time given will return current time
iso_date_time = parse_dt_str(" ".join(sys.argv[2:]))

forecast = call_forecast_api(stop_data["stop_lat"], stop_data["stop_lon"], iso_date_time)

pretty_weather = prettify_forcast(forecast)

print "location: " + stop_data['stop_name']
print "time: " + iso_date_time

for key, value in pretty_weather.iteritems():
	print key + " - " + value