import sys
from termcolor import colored, cprint
from Map import *
from Node import *

class Path:
	def __init__(self):
		self.startNode = None
		self.endNode = None
		self.nodes = []

	def printPath(self, size):
		pathIcon = "X"
		color = "green"
		output = "\n"
		print "start: %d, %d\n" % (self.nodes[0].x, self.nodes[0].y)
		print "end  : %d, %d\n" % (self.nodes[-1].x, self.nodes[-1].y)
		for y in range(size[1]):
			for x in range(size[0]):
				color = "green"
				if( x == self.nodes[0].x and y == self.nodes[0].y ):
					color = "yellow"
				elif( x == self.nodes[-1].x and y == self.nodes[-1].y ):
					color = "red"
				
				if( not self.checkCoordsInList(self.nodes, (x, y)) ):
					output += "  "
				else:
					output += colored(pathIcon + " ", color)
			output += "\n"

		print output

	def checkCoordsInList(self, list, node):
		return any((obj.x == node[0] and obj.y == node[1]) for obj in list)