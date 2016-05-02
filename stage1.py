#!/usr/bin/python

import sys
import os.path
from stops import csv_extract_list, validate_stop_name
from forecast import call_forecast_api

# Path to the stops file
STOPS_FILE_PATH = "stops.txt"

# Validate usage
if len(sys.argv) < 2:
	print "Usage: " + sys.argv[0] + " <stop name> <time>"
	exit()

# Validate stops file exists
if not os.path.exists(STOPS_FILE_PATH):
	print "Error: Could not find stops file at path " + STOPS_FILE_PATH
	exit()

# Stop name is always the first arg
stop_name = sys.argv[1]
# Everything after is time
time_string = " ".join(sys.argv[2:-1])

# List of stops is in a file, so get the list from it
stops_list = csv_extract_list(STOPS_FILE_PATH)
# Validate the users input against the list of stops
valid_stops = validate_stop_name(stop_name, stops_list)

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
forecast = call_forecast_api(valid_stop["stop_lat"], valid_stop["stop_lon"])

## We need to prettify the forecast data into human readable output

# Assign variable names for readability
temperature = forecast["currently"]["temperature"]
rain_chance = forecast["currently"]["precipProbability"]
rain_intensity = forecast["currently"]["precipIntensity"]
wind_speed = forecast["currently"]["windSpeed"]
wind_direction = forecast["currently"]["windBearing"]

## Now build strings for printing
## Rain amount and wind direction are a bit tricky so let's do them first

# Convert rain amount in mm/hr into a classification of:
# None, Light, Moderate, Heavy
if rain_intensity < 0.05:
	rain_intensity_str = "None"
elif rain_intensity < 0.5:
	rain_intensity_str = "Light"
elif rain_intensity < 2.5:
	rain_intensity_str = "Moderate"
else: #rain intensity is >2.5
	rain_intensity_str = "Heavy"

# Convert wind direction in degrees to compass directions
# N, NE, E, SE, S, SW, W, NW
# 0, 45, 90, 135, 180, 225, 270, 315
# The final string is determined by 45 degrees wedges, or,
# 22.5 degrees either side of each exact direction
# I hope that made sense, else look at a compass

if wind_direction == None:
	#API Docs says if wind dir is 0, it isn't even returned in the api call
	wind_direction_str = "N"
elif wind_direction > 337.5 or wind_direction <= 22.5:
	wind_direction_str = "N"
elif wind_direction <= 67.5:
	wind_direction_str = "NE"
elif wind_direction <= 112.5:
	wind_direction_str = "E"
elif wind_direction <= 157.5:
	wind_direction_str = "SE"
elif wind_direction <= 202.5:
	wind_direction_str = "S"
elif wind_direction <= 247.5:
	wind_direction_str = "SW"
elif wind_direction <= 292.5:
	wind_direction_str = "W"
elif wind_direction <= 337.5:
	wind_direction_str = "NW"
else:
	# Something bad happened
	wind_direction_str = "Error"

# Convert rain chance from decimal to percentage value
rain_chance = int(rain_chance * 100)


## Finally print everything out

# Print temperature
print "Temp - celsius: %0.2f" % (temperature)

# Print rain
print "Rain - chance: %d%%, intensity: %s" % (rain_chance, rain_intensity_str) 

# Print wind
print "Wind - speed: %0.2fm/s, direction: %s" % (wind_speed, wind_direction_str)