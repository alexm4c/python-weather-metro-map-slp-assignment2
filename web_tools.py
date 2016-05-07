#!/usr/bin/python

def htmlify(content):
	data = "<!DOCTYPE html>\n<html>\n"

	if content["title"]:
		data += "\t<head><title>" + content["title"] + "</title></head>\n"

	if content["body"]:
		data += "\t<body>\n\t\t<table>\n"
		for key, value in content["body"].iteritems():
			data += "\t\t\t<tr>\n"
			data += "\t\t\t\t<td>" + key + "</td><td>" + value + "</td>\n"
			data += "\t\t\t</tr>\n"

		data += "\t\t</table>\n\t</body>\n"


	data += "</html>"

	return data