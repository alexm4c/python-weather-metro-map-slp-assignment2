#!/usr/bin/python

def pageify(content):
	# Takes a dictionary as input with keys title and body.
	# Title is the title of the web page and
	# body is a list of string elements to append to the page

	data = "<!DOCTYPE html>\n<html>\n"

	if content["title"]:
		data += "<head><title>" + content["title"] + "</title></head>\n"

	if content["body"]:
		data += "<body>\n"

		if isinstance(content["body"], list):
			for elem in content["body"]:
				data += elem

		data += "\n</body>\n"

	data += "</html>"

	return data


def tableify(content):
	# Takes a dictionary as input and returns a 
	# html table representation of it as string.

	data = ""

	if isinstance(content, dict):
		data += "<table>\n"
		for key, value in content.iteritems():
			data += "<tr>\n"
			data += "<td>" + key + "</td><td>" + value + "</td>\n"
			data += "</tr>\n"
		data += "</table>\n"


	return data


