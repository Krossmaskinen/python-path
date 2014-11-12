from Map import *
from Node import *
from Path import *
import Globals

import operator

class Pathfinder:
	_map = None

	def __init__(self, pMap):
		self.debug = True
		self.openList = []
		self.closedList = []
		self.targetFound = False

		if( not self._map ):
			self._map = pMap

	def resetPath(self, nodes):
		del self.closedList[:]
		del self.openList[:]
		self.targetFound = False
		for node in nodes:
			node.parentNode = None

	def findPath(self, start, end):
		self.resetPath(self._map.nodes)
		"""Initializes the A* to find a way from start to end, based on the nodes in self._map"""		
		self.targetFound = False
		currentNode = self._map.getNode((start[0], start[1]))
		targetNode = self._map.getNode((end[0], end[1]))

		# cancel if the target is unreachable
		if( targetNode.type == self._map.types["wall"]):
			return None
		elif( Globals.gEntities ):
			pathClear = self.checkEntityCollision( end )
			if( not pathClear ):
				return None

		# add the starting node to the list and start the A*
		self.openList.append(currentNode)
		index = len(self.openList) - 1

		# as long as there're items in the open list and the target is not found, keep searching
		while(len(self.openList) and not self.targetFound):
			self.checkNode(start, end )

		# if the target is found, extract the path and return it, otherwise return None
		if(self.targetFound):
			path = Path()
			self.extractPath(path)
			return path
		else:
			return None
		
	def checkNode(self, start, end):
		"""Updates the A* algorithm one step"""
		# move the first node of open list to the closed list
		currentNode = self.openList.pop(0)
		self.closedList.append(currentNode)

		# check if the current node, that is, the last one added to the closed list, is the taget node
		if( currentNode.pos[0] == end[0] and currentNode.pos[1] == end[1] ):
			# target found! VICORY! return true!!
			self.targetFound = True
			return True

		# add neighbours to openList
		self.checkNeighbours(currentNode, start, end)

		# sort openList on F value
		self.openList.sort(key = operator.attrgetter("F"))

		# no path found yet
		return False

	def checkNeighbours(self, currentNode, start, end):
		"""Check for walkable neighbours to the current node being checked"""
		for key in currentNode.neighbours:
			neighbour = currentNode.neighbours[key]

			# check if node is in closed list and in open list
			nodeInClosedList = self.checkIfInList(self.closedList, neighbour['node'])
			nodeInOpenList = self.checkIfInList(self.openList, neighbour['node'])

			# check if node is walkable
			nodeWalkable = False
			if(neighbour['node'].type == self._map.types["open"]):
				# check if a horizontal/vertical neighbour is a wall. If so it's not walkable
				nodeWalkable = True

			if( nodeWalkable and Globals.gEntities ):
				nodeWalkable = self.checkEntityCollision( (neighbour['node'].pos[0], neighbour['node'].pos[1]) )

			if( nodeInClosedList == False and nodeWalkable ):
				# set parent
				self.checkNewParent(neighbour, currentNode)
				# calculate H - the distance between this node and the end node
				neighbour['node'].H = self.getHeuristics(neighbour['coords'], end)
				# calculate F
				neighbour['node'].F = neighbour['node'].G + neighbour['node'].H
				# add to open list if not already in it
				if( not self.checkIfInList(self.openList, neighbour['node']) ):
					self.openList.append(neighbour['node'])

	def checkNewParent(self, neighbour, pParent):
		"""Calculate G - the G value of the parent plus the G value of this node relative to it's parent between this node and the starting node
		check if this node has a parent. If not, set currentNode as the parent. If it has, compare the parent's G + this node's G and currentNode's G + this node's G.
		Set whatever node that gives the lowest G value as the parent"""
		if( not neighbour['node'].parentNode):
			neighbour['node'].parentNode = pParent
			neighbour['node'].G = pParent.G + neighbour['g']
		elif( pParent.G + neighbour['g'] < neighbour['node'].parentNode.G + neighbour['g'] ):
			neighbour['node'].parentNode = pParent
			neighbour['node'].G = pParent.G + neighbour['g']

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
		return node.pos[0] + node.pos[1] * mapWidth

	def checkIfInList(self, list, node):
		"""Returns True if the node is in the passed in list, based on the x and y coordinates, else False"""
		return any((obj.pos[0] == node.pos[0] and obj.pos[1] == node.pos[1]) for obj in list)

	def checkEntityCollision(self, pos):
		for entity in Globals.gEntities:
			entityPos = entity.getTilePos()
			if( entityPos[0] == pos[0] and entityPos[1] == pos[1] ):
				return False

		return True