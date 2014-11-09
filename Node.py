class Node:
	#types:
	# 0 - open
	# 1 - wall

	def __init__(self, coordinates, type, mapSize, pMap, name = ""):
		self.name = name
		self.x = coordinates[0]
		self.y = coordinates[1]
		self.type = type

		self.G = 0 # distance from starting point (will vary depending on what node is accessing it)
		self.H = 0 # distance from target point
		self.F = 0 # total distance from starting point to target point
		self.parentNode = None

		self.neighbours = {}

		self.mapWidth = mapSize[0]
		self.mapHeight = mapSize[1]

		#self.calculateNeighbours(pMap)

	def printName(self):
		print(self.name)

	def printCoordinates(self):
		print(self.x)
		print(self.y)

	def calculateNeighbours(self, pMap):
		"""
			Making it easier for the pathfinder to find the neighbours
			straight = 10 G points
			diagonal = 14 G points
			Must be called after the entire map is loaded
		"""

		if(self.y > 0):
			coord = self.get1DCoordinate((self.x, self.y - 1))
			self.neighbours['top'] = self.createNeighbour((self.x, self.y - 1), pMap.nodes[coord], 10)
			if(self.x > 0):
				coord = self.get1DCoordinate((self.x - 1, self.y - 1))
				self.neighbours['top left'] = self.createNeighbour((self.x - 1, self.y - 1), pMap.nodes[coord], 14)
			if(self.x < self.mapWidth - 1):
				coord = self.get1DCoordinate((self.x + 1, self.y - 1))
				self.neighbours['top right'] = self.createNeighbour((self.x + 1, self.y - 1), pMap.nodes[coord], 14)

		if(self.x > 0):
			coord = self.get1DCoordinate((self.x - 1, self.y))
			self.neighbours['left'] = self.createNeighbour((self.x - 1, self.y), pMap.nodes[coord], 10)
		if(self.x < self.mapWidth - 1):
			coord = self.get1DCoordinate((self.x + 1, self.y))
			self.neighbours['right'] = self.createNeighbour((self.x + 1, self.y), pMap.nodes[coord], 10)

		if(self.y < self.mapHeight - 1):
			coord = self.get1DCoordinate((self.x, self.y + 1))
			self.neighbours['bottom'] = self.createNeighbour((self.x, self.y + 1), pMap.nodes[coord], 10)
			if(self.x > 0):
				coord = self.get1DCoordinate((self.x - 1, self.y + 1))
				self.neighbours['bottom left'] = self.createNeighbour((self.x - 1, self.y + 1), pMap.nodes[coord], 14)
			if(self.x < self.mapWidth - 1):
				coord = self.get1DCoordinate((self.x + 1, self.y + 1))
				self.neighbours['bottom right'] = self.createNeighbour((self.x + 1, self.y + 1), pMap.nodes[coord], 14)

		# remove neighbours that cut corners if top, right, bottom or left is a wall
		if( 'top' in self.neighbours and self.neighbours['top']['node'].type == 1 ):
			self.neighbours.pop('top left', None)
			self.neighbours.pop('top right', None)
		if( 'right' in self.neighbours and self.neighbours['right']['node'].type == 1 ):
			self.neighbours.pop('top right', None)
			self.neighbours.pop('bottom right', None)
		if( 'bottom' in self.neighbours and self.neighbours['bottom']['node'].type == 1 ):
			self.neighbours.pop('bottom right', None)
			self.neighbours.pop('bottom left', None)
		if( 'left' in self.neighbours and self.neighbours['left']['node'].type == 1 ):
			self.neighbours.pop('bottom left', None)
			self.neighbours.pop('top left', None)

	def createNeighbour(self, coords, node, g):
		return {
			"coords": coords,
			"node": node,
			"g": g
		}

	def get1DCoordinate(self):
		return self.x + self.y * self.mapWidth

	def get1DCoordinate(self, coords):
		return coords[0] + coords[1] * self.mapWidth

	def getTilePos(self):
		return ( int(self.x + 0.5), int(self.y + 0.5) )