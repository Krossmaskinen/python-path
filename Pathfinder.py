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
		"""Initializes the A* to find a way from start to end, based on the nodes in pMap"""
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
		closedPath = Path()
		while(len(self.openList)):
			# if target is found or all nodes have been checked, the search is finished
			# bulle = raw_input(">")
			# closedPath.nodes = self.closedList
			# pMap.printMapWithPath(closedPath)
			if(self.checkNode(pMap, start, end)):
				break

		if(self.targetFound):
			path = Path()
			self.extractPath(path)
			return path
		else:
			return None
		
	def checkNode(self, pMap, start, end):
		"""Updates the A* algorithm one step"""
		# move the first node of open list to the closed list
		currentNode = self.openList[0]
		self.closedList.append(currentNode)
		del self.openList[0]

		# check if the current node, that is, the last one added to the closed list, is the taget node
		if( currentNode.x == end[0] and currentNode.y == end[1] ):
			# target found! VICORY! return true!!
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
			if(neighbour['node'].type == pMap.types["open"]):
				# check if a horizontal/vertical neighbour is a wall. If so it's not walkable

				# if( key == "top left" ):
				# 	if( currentNode.neighbours['top']['node'].type == pMap.types["wall"] or currentNode.neighbours['left']['node'].type == pMap.types["wall"] ):
				# 		nodeWalkable = False
				# elif( key == "top right" ):
				# 	if( currentNode.neighbours['top']['node'].type == pMap.types["wall"] or currentNode.neighbours['right']['node'].type == pMap.types["wall"] ):
				# 		nodeWalkable = False
				# elif( key == "bottom left" ):
				# 	if( currentNode.neighbours['bottom']['node'].type == pMap.types["wall"] or currentNode.neighbours['left']['node'].type == pMap.types["wall"] ):
				# 		nodeWalkable = False
				# elif( key == "bottom right" ):
				# 	if( currentNode.neighbours['bottom']['node'].type == pMap.types["wall"] or currentNode.neighbours['right']['node'].type == pMap.types["wall"] ):
				# 		print "yeah"
				# 		nodeWalkable = False
				# else:
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
		"""Returns the H value for the node with coords1 relative to the node with coords2"""
		dx = abs(coords1[0] - coords2[0])
		dy = abs(coords1[1] - coords2[1])
		return 10 * (dx + dy)

	def extractPath(self, pPath):
		"""Loads the found path into a class Path object"""
		# last element in the closedList will be the target node if one was found
		currentNode = self.closedList[-1]
		pPath.nodes.append(currentNode)

		# steps through all the parents from the target node to the start node and add them to the path
		while(currentNode):
			pPath.nodes.append(currentNode)
			currentNode = currentNode.parentNode

		# make the path go from start to target instead of the other way around
		pPath.nodes.reverse()

	def get1DCoordinate(self, node, mapWidth):
		"""Returns the map list index for the current node based on the x and y coordinates"""
		return node.x + node.y * mapWidth

	def checkIfInList(self, list, node):
		"""Returns True if the node is in the passed in list, based on the x and y coordinates, else False"""
		return any((obj.x == node.x and obj.y == node.y) for obj in list)