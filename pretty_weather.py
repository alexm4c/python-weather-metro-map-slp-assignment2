TARGET_BLOCK = "currently"

def prettify_forcast(forecast):

	# Assign variable names for readability
	temperature 	= forecast[TARGET_BLOCK]["temperature"]
	rain_chance 	= forecast[TARGET_BLOCK]["precipProbability"]
	rain_intensity 	= forecast[TARGET_BLOCK]["precipIntensity"]
	wind_speed 		= forecast[TARGET_BLOCK]["windSpeed"]
	wind_direction 	= forecast[TARGET_BLOCK]["windBearing"]

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

	# Print temperature
	pretty_weather["temp"] = "celsius: %0.2f" % (temperature)

	# Print rain
	pretty_weather["rain"] = "chance: %d%%, intensity: %s" % (rain_chance, rain_intensity_str) 

	# Print wind
	pretty_weather["wind"] = "speed: %0.2fm/s, direction: %s" % (wind_speed, wind_direction_str)

	return pretty_weather