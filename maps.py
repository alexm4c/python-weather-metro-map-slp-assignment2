#!/usr/bin/python

from PIL 		import Image, ImageDraw, ImageColor, ImageFont
from itertools 	import izip

class MapImage():
	"""

	MapImage class holds data asscociated with overlaying images over it.

	imgPath: path to the original map image
	saveTo: where to save the resulting overlaid image
	bounds: the GPS boundaries of the map for calculating interpolation to pixels

	"""

	def __init__(self, imgPath, saveTo, eastBound, southBound, westBound, northBound):
		
		self.img = Image.open(imgPath)
		self.img = self.img.resize([2560, 2560])

		self.saveTo = saveTo
		
		(self.imgWidth, self.imgHeight) = self.img.size
		self.westBound = westBound
		self.southBound = southBound
		self.eastBound = eastBound
		self.northBound = northBound

	### end of __init__ ###

	def coordsToPixels(self, latitude, longitude):
		"""

		Input: GPS coordinates, latitude and longitude.
		Output: Pixels asscociated with those coordinates

		"""
		geoLength = float(self.eastBound - self.westBound)
		geoHeight = float(self.northBound - self.southBound)

		yScale = float(self.imgHeight / geoHeight)
		xScale = float(self.imgWidth / geoLength)

		xPixel = int(xScale * (self.eastBound - longitude))
		yPixel = int(yScale * (self.northBound - latitude))

		return (xPixel, yPixel)

	### end of coordsToPixels ###

	def drawStations(self, coordList, nameList):
		"""
		
		From a list of coordinates and names,
		overlay those onto the map image.

		"""

		draw = ImageDraw.Draw(self.img) 

		for index, (coord, name) in enumerate(izip(coordList, nameList)):

			(x, y) = coord

			draw.rectangle([x, y, x+5, y+5], fill=255)

			draw.text([x+9, y-2], name, fill=0)
			draw.text([x+8, y-3], name, fill=255)

		self.img.save(self.saveTo, "PNG")

	### end of drawStations ###

### end of class MapImage ###