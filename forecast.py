#!/usr/bin/python

import urllib2
import json

API_URL = "https://api.forecast.io/forecast/"
API_KEY = "3263712d1c1452735faa19a7f9b90edc"
OPTIONS = "?units=si&exclude=minutely,hourly,daily,alerts,flags"

### call_forecast_api ###
# Calls the forcast api given above, 
# then converts the returned JSON into
# a usable dictionary.

def call_forecast_api(latitude, longitude, date_time):
	
	# build up api call url
	url =  API_URL 
	url += API_KEY 
	url += "/"
	url += latitude 
	url += "," 
	url += longitude
	url += ","
	url += date_time
	url += OPTIONS

	# make the api call and store returned json data
	forecast_json = urllib2.urlopen(url).read()
	# convert json to dictionary
	forecast = json.loads(forecast_json)

	return forecast

### end of get_forecast ###


### prettify_forecast ###
# Helper function that converts a
# dictionary of assumed structure
# into more human friendly output
# strings as dictionary eg.
# "wind":"2m/s N"
# Makes changes such as turning rain intensity
# in mm/hr into classes,
# and wind bearing into compass direction

def prettify_forcast(forecast):

	# Assign variable names for readability
	temperature 	= forecast["currently"]["temperature"]
	rain_chance 	= forecast["currently"]["precipProbability"]
	rain_intensity 	= forecast["currently"]["precipIntensity"]
	wind_speed 		= forecast["currently"]["windSpeed"]
	wind_direction 	= forecast["currently"]["windBearing"]

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

	pretty_weather = dict()

	pretty_weather["temp"] = "celsius: %0.2f" % (temperature)
	pretty_weather["rain"] = "chance: %d%%, intensity: %s" % (rain_chance, rain_intensity_str) 
	pretty_weather["wind"] = "speed: %0.2fm/s, direction: %s" % (wind_speed, wind_direction_str)

	return pretty_weather

### end of prettify_forcast ###