import pygame

from Map import *

class GraphicsManager:
	def __init__(self, pMap):
		self.size = width, height = pMap.width * pMap.tileSize, pMap.height * pMap.tileSize
		self.images = {}
		self.tileSize = pMap.tileSize
		self.initWindow(self.size)
		self.loadImages()

	def loadImages(self):
		self.typeImages = {
			"open": "open.png",
			"wall": "wall.png",
			"path": "path.png",
			"start": "start.png",
			"end": "end.png",
			"ninja": "ninja.png"
		}
		for key in self.typeImages:
			self.images[key] = pygame.image.load(self.typeImages[key])
			self.images[key] = pygame.transform.scale( self.images[key], (self.tileSize, self.tileSize) )

	def initWindow(self, size):
		"""Initializes pygame window"""
		self.screen = pygame.display.set_mode(size)

	def render(self, pMap, pPath, pEntity):
		self.screen.fill( (0,0,0) )
		self.printMap(pMap)
		# sometimes there might not be a path to display
		if(pPath):
			self.printPath(pPath)

		self.printEntity(pEntity)
		pygame.display.flip()

	def printMap(self, pMap):
		for y in range(pMap.height):
			for x in range(pMap.width):
				i = x + pMap.width * y
				coords = (x * self.tileSize, y * self.tileSize)
				currentTile = pMap.nodes[i]
				if(currentTile.type == pMap.types["wall"]):
					self.screen.blit(self.images["wall"], coords)
				elif(currentTile.type == pMap.types["open"]):
					self.screen.blit(self.images["open"], coords)

	def printPath(self, pPath):
		for i in range(len(pPath.nodes)):
			node = pPath.nodes[i]
			coords = (node.x * self.tileSize, node.y * self.tileSize)
			if(i == len(pPath.nodes) - 1):
				self.screen.blit(self.images["end"], coords)
			elif(i != 0):
				self.screen.blit(self.images["path"], coords)
			else:
				self.screen.blit(self.images["start"], coords)

	def printEntity(self, pEntity):
		coords = (pEntity.pos[0] * self.tileSize, pEntity.pos[1] * self.tileSize)
		self.screen.blit(self.images["ninja"], coords)