from Map import *
from Node import *
from Path import *
import operator

class Pathfinder:
	def __init__(self):
		self.openList = []
		self.closedList = []
		self.targetFound = False

	def findPath(self, pMap, start, end):
		print "%d, %d \n" % start
		print "%d, %d \n" % end
		
		self.targetFound = False
		currentNode = pMap.getNode((start[0], start[1]))
		targetNode = pMap.getNode((end[0], end[1]))

		# cancel if the target is unreachable
		if(targetNode.type == pMap.types["wall"]):
			return None

		self.openList.append(currentNode)
		index = len(self.openList) - 1
		
		# while(len(self.openList) > 0):
		j = 0
		while(len(self.openList) and j < 2000):
			if(self.checkNode(pMap, start, end)):
				break
			j += 1
		print j

		if(self.targetFound):
			path = Path()
			self.extractPath(path)
			print "target: %d, %d \n" % (self.closedList[-1].x, self.closedList[-1].y)
			return path
		else:
			return None
		
	def checkNode(self, pMap, start, end):
		currentNode = self.openList[0]
		self.closedList.append(currentNode)
		del self.openList[0]

		# check if the current node, that is, the last one added to the closed list, is the taget node
		if( currentNode.x == end[0] and currentNode.y == end[1] ):
			print "found: %d, %d\n" % (end[0], end[1])
			print "node: %d, %d\n" % (currentNode.x, currentNode.y)
			# target found! abort! abort!!
			self.targetFound = True
			return True

		# add neighbours to openList
		for key in currentNode.neighbours:
			neighbour = currentNode.neighbours[key]

			# check if node is in closed list and in open list
			nodeInClosedList = self.checkIfInList(self.closedList, neighbour['node'])
			nodeInOpenList = self.checkIfInList(self.openList, neighbour['node'])

			# check if node is walkable
			nodeWalkable = False
			if (neighbour['node'].type == pMap.types["open"]):
				nodeWalkable = True

			if( nodeInClosedList == False and nodeWalkable ):
				# calculate G - the G value of the parent plus the G value of this node relative to it's parent between this node and the starting node
				# check if this node has a parent. If not, set currentNode as the parent. If it has, compare the parent's G + this node's G and currentNode's G + this node's G.
				# Set whatever node that gives the lowest G value as the parent
				if( not neighbour['node'].parentNode):
					neighbour['node'].parentNode = currentNode
					neighbour['node'].G = currentNode.G + neighbour['g']
				elif( currentNode.G + neighbour['g'] < neighbour['node'].parentNode.G + neighbour['g'] ):
					neighbour['node'].parentNode = currentNode
					neighbour['node'].G = currentNode.G + neighbour['g']

				# calculate H - the distance between this node and the end node
				neighbour['node'].H = self.getHeuristics(neighbour['coords'], end)

				# calculate F
				neighbour['node'].F = neighbour['node'].G + neighbour['node'].H
				# add to open list

				if( not self.checkIfInList(self.openList, neighbour['node']) ):
					self.openList.append(neighbour['node'])

		# sort openList on F value
		self.openList.sort(key = operator.attrgetter("F"))

		# no path found yet
		return False

	def getHeuristics(self, coords1, coords2):
		dx = abs(coords1[0] - coords2[0])
		dy = abs(coords1[1] - coords2[1])
		return 10 * (dx + dy)

	def extractPath(self, pPath):
		"""Loads the found path into a class Path object"""
		# last element in the closedList will be the target node if one was found
		currentNode = self.closedList[-1]
		pPath.nodes.append(currentNode)
		while(currentNode):
			pPath.nodes.append(currentNode)
			currentNode = currentNode.parentNode

		pPath.nodes.reverse()

		print "path length: %d" % len(pPath.nodes)

	def get1DCoordinate(self, node, mapWidth):
		return node.x + node.y * mapWidth

	def checkIfInList(self, list, node):
		return any((obj.x == node.x and obj.y == node.y) for obj in list)

	def printPath(self):
		"""to be continued"""