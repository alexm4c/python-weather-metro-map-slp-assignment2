#!/usr/bin/python

import urllib2
import json

API_URL = "https://api.forecast.io/forecast/"
API_KEY = "3263712d1c1452735faa19a7f9b90edc"
OPTIONS = "?units=si&exclude=minutely,hourly,daily,alerts,flags"

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