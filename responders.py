#!/usr/bin/python
from collections 	import OrderedDict
from metro 			import metro_data
from parsedt 		import parse_dt_str
from forecast 		import call_forecast_api, prettify_forcast
from web_tools 		import pageify, tableify

# this is suitable for a GET - it has no parameters
def initialPage():

	with open("index.html") as index_fo:
		response = index_fo.read()

	return response

# this is suitable for a POST - it has a single parameter which is 
# a dictionary of values from the web page form.

def respondToSubmit(formData):
	
	response = dict()
	response["title"] = "Prognostication"
	response["body"] = list()
	
	# must validate the form names
	# they could be anything!
	if formData["stop_name"]:
		stop_name = formData["stop_name"]
	else:
		response["body"].append("No stop name given!")
		return pageify(response)

	if formData["datetime"]:
		dt_string = formData["datetime"]
	else:
		dt_string = 0

	stop_data = metro_data().find_stop(stop_name)
	if not stop_data:
		response["body"].append("Could not find stop by name " + stop_name)
		return pageify(response)

	iso_date_time = parse_dt_str(dt_string)

	forecast = call_forecast_api(stop_data["stop_lat"], stop_data["stop_lon"], iso_date_time)

	weather_table = OrderedDict()
	weather_table["location"] = stop_data['stop_name']
	weather_table["time"] = iso_date_time
	weather_table.update(prettify_forcast(forecast))
	weather_table = tableify(weather_table)

	response["body"].append(weather_table)

	return pageify(response)