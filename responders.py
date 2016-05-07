#!/usr/bin/python
from collections import OrderedDict
from metro import metro_data
from parsedt import parse_dt_str
from forecast import call_forecast_api, prettify_forcast
import web_tools

# this is suitable for a GET - it has no parameters
def initialPage():

	with open("index.html") as index_fo:
		response = index_fo.read()

	return response

# this is suitable for a POST - it has a single parameter which is 
# a dictionary of values from the web page form.

def respondToSubmit(formData):
	
	# must validate the form names
	# they could be anything!
	if formData["stop_name"]:
		stop_name = formData["stop_name"]
	else:
		response = "No stop name given!"
		return response

	if formData["datetime"]:
		dt_string = formData["datetime"]
	else:
		dt_string = 0

	stop_data = metro_data().find_stop(stop_name)
	if not stop_data:
		response = "Could not find stop by name " + stop_name
		return response

	iso_date_time = parse_dt_str(dt_string)

	forecast = call_forecast_api(stop_data["stop_lat"], stop_data["stop_lon"], iso_date_time)
	pretty_weather = prettify_forcast(forecast)

	response = dict()
	response["title"] = "Prognostication"

	response["body"] = OrderedDict()
	response["body"]["location"] = stop_data['stop_name']
	response["body"]["time"] = iso_date_time

	for key, value in pretty_weather.iteritems():
		response["body"][key] = value

	return web_tools.htmlify(response)