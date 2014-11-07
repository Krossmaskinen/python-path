import sys
from termcolor import colored, cprint
from Node import *

class Map:

	def __init__(self):
		# map node type
		self.types = {"open": 0, "wall": 1}
		self.nodes = []
		self.wallColor = (0, 0, 0)
		self.roadColor = (255, 255, 255)
		self.width = 0
		self.height = 0

	def printMap(self):
		wallIcon = "0"
		output = "\n"

		for y in range(self.height) + 2:
			for x in range(self.width) + 2:
				if(x == 0 or x == self.width or y == 0 or y == self.height):
					output += wallIcon + " "
					continue

				# get one dimensional coordinate from two dimensional coordinates
				currentCoord = x + self.width * y
				if(self.nodes[currentCoord].type == self.types["wall"]):
					output += wallIcon + " "
				elif(self.nodes[currentCoord].type == self.types["open"]):
					output += "  "
			output += "\n"

		print output

	def loadMap(self, pMap, width, height):
		self.width = width
		self.height = height

		for y in range(height):
			for x in range(width):
				# get one dimensional coordinate from two dimensional coordinates
				currentCoord = x + width * y
				if(pMap[currentCoord] == self.wallColor):
					self.nodes.append(Node((x, y), 1, (self.width, self.height), self))
				elif(pMap[currentCoord] == self.roadColor):
					self.nodes.append(Node((x, y), 0, (self.width, self.height), self))

		for y in range(height):
			for x in range(width):
				currentCoord = x + width * y
				self.nodes[currentCoord].calculateNeighbours(self)

	def getNode(self, coordinates):
		index = coordinates[0] + self.width * coordinates[1]
		return self.nodes[index]

	def printMapWithPath(self, path):
		wallIcon = "0"
		pathIcon = "X"
		output = "\n"

		for y in range(self.height):
			for x in range(self.width):
				if( len(path.nodes) > 0 and path.nodes[-1].x == x and path.nodes[-1].y == y ):
					output += colored(pathIcon + " ", "red")
				elif( len(path.nodes) > 0 and path.nodes[0].x == x and path.nodes[0].y == y ):
					output += colored(pathIcon + " ", "yellow")
				elif( path.checkCoordsInList(path.nodes, (x, y)) ):
					output += colored(pathIcon + " ", 'green')
				else:
					# get one dimensional coordinate from two dimensional coordinates
					currentCoord = x + self.width * y
					if(self.nodes[currentCoord].type == self.types["wall"]):
						output += wallIcon + " "
					elif(self.nodes[currentCoord].type == self.types["open"]):
						output += "  "

			output += "\n"

		print output