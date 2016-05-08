#!/usr/bin/python
from collections 	import OrderedDict
from metro 			import metro_data
from parsedt 		import parse_dt_str
from forecast 		import call_forecast_api, prettify_forcast
from web_tools 		import pageify, tableify

# this is suitable for a GET - it has no parameters
def initialPage():

	response = dict()
	response["title"] = "Prognosticator"
	response["body"] = list()

	# prepare the station list element
	station_select = "<select name=\"stop_name\">\n"
	for stop in metro_data().stop_list:
		station_select += "<option>"
		station_select += stop["stop_name"]
		station_select += "</option>\n"
	station_select += "</select>\n"


	form = "<form action=\"http://127.0.0.1:34567/\" method=\"POST\">"
	form += "Station Name: "
	form += station_select
	form += "Time: "
	form += "<input type=\"text\" name=\"datetime\"/>"
	form += "<input type=\"submit\" value=\"Go!\">"
	form += "</form>"

	response["body"].append(form)

	return pageify(response)

# this is suitable for a POST - it has a single parameter which is 
# a dictionary of values from the web page form.

def respondToSubmit(formData):
	
	response = dict()
	response["title"] = "Prognostication"
	response["body"] = list()
	
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