#!/usr/bin/python

from datetime import datetime
import re

day_name_pattern = r'(?:Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)'
day_specifier_pattern = r'(' + day_name_pattern + '|today|now|tomorrow|next week)'
date_pattern = r'(?:(\d+) day(?:s)? from )?' + day_specifier_pattern

time_12hr_pattern = r'\b([0-9]|0[0-9]|1[0-2]):([0-5][0-9])\s*(am|pm)\b'
time_24hr_pattern = r'\b([0-9]|0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])\b'


def string2unix_time(datetime_string):

	# matching out date information
	mo = re.match(date_pattern, datetime_string, re.I)
	
	if mo:
		days_from = mo.group(1)
		day_specifier = mo.group(2)

	# matching out time information
	mo = re.search(time_12hr_pattern, datetime_string, re.I)

	if mo:
		print mo.group()
		hours = int(mo.group(1))

		minutes = int(mo.group(2))
		isPM = (mo.group(3).lower() == 'pm')

		# converting to 24hr
		if isPM and hours != 12:
			hours += 12
		elif not isPM and hours == 12:
			hours = 0

	else: # did not match 12hr time
		# do another match for 24hr time
		mo = re.search(time_24hr_pattern, datetime_string, re.I)

		if mo:
			hours = int(mo.group(1))
			minutes = int(mo.group(2))

		else: # did not match any time
			hours = "something went wrong"
			minutes = "so wrong"
			# return current time




	return days_from, day_specifier, hours, minutes

print string2unix_time("14:00")