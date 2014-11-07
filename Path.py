from Map import *
from Node import *

class Path:
	def __init__(self):
		self.startNode = None
		self.endNode = None
		self.nodes = []

	def printPath(self, size):
		pathIcon = "0"
		output = "\n"
		for x in range(size[0]):
			for y in range(size[1]):
				if( not self.checkCoordsInList(self.nodes, (x, y)) ):
					output += "  "
				else:
					output += pathIcon + " "
			output += "\n"

		print output

	def checkCoordsInList(self, list, node):
		return any((obj.x == node[0] and obj.y == node[1]) for obj in list)