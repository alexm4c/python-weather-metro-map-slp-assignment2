#!/usr/bin/python

from datetime import datetime, time, timedelta
import re

day_name_pattern = r'(?:Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)'
day_specifier_pattern = r'(' + day_name_pattern + '|today|now|tomorrow|next week)'
date_pattern = r'(?:(\d+) day(?:s)? from )?' + day_specifier_pattern

time_12hr_pattern = r'\b([0-9]|0[0-9]|1[0-2]):([0-5][0-9])\s*(am|pm)\b'
time_24hr_pattern = r'\b([0-9]|0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])\b'

### get_weekday_value ###
# returns a number representation associated
# with a day of the week. These values correspond
# to the values assigned by the datetime library

def get_weekday_value(string):
	string = string.lower()

	# value returned corresponds to the same value assigned
	# by the datetime library

	if string == 'mon' or string == 'monday':
		return 0
	elif string == 'tue' or string == 'tuesday':
		return 1
	elif string == 'wed' or string == 'wednesday':
		return 2
	elif string == 'thu' or string == 'thursday':
		return 3
	elif string == 'fri' or string == 'friday':
		return 4
	elif string == 'sat' or string == 'saturday':
		return 5
	elif string == 'sun' or string == 'sunday':
		return 6
	else:
		return None

### end of get_weekday_value ###


### parse_dt_str ###
# This function takes a single string in
# the format specified in the assigment specs
# and returns a ISO format date time, ready
# to pass to the weather API.

def parse_dt_str(datetime_string):

	today = datetime.today()

	## First parse the date selected
	## If no date is found, defaults to today

	mo = re.match(date_pattern, datetime_string, re.I)
	
	if mo:
		day_modifier = mo.group(1)
		day_selector = mo.group(2).lower()
	else:
		day_selector = None

	if day_modifier:
		day_modifier = int(day_modifier)
	else:
		day_modifier = 0

	if day_selector == None:
		pass
	elif day_selector == 'today' or day_selector == 'now':
		# day is already today, no need to change
		pass
	elif day_selector == 'tomorrow':
		day_modifier += 1
	elif day_selector == 'next week':
		day_modifier += 7
	else: #day selector MUST be weekday
		# difference between selected and current
		wd_modifier = get_weekday_value(day_selector) - today.weekday()

		if wd_modifier < 0:
			wd_modifier = 7 + wd_modifier

		day_modifier += wd_modifier

	selected_date = today + timedelta(days=day_modifier)

	## Then parse time selected
	## if no time is found, time is assumed to be the current time

	mo = re.search(time_12hr_pattern, datetime_string, re.I)

	if mo:
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
			# current time
			hours = today.hour
			minutes = today.minute

	selected_time = time(hours, minutes, 0)

	return datetime.combine(selected_date, selected_time).isoformat()

### end of parse_dt_str ###