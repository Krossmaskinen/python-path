from PIL import Image
import sys
import pygame

from Map import *
from Node import *
from Path import *
from Pathfinder import *
from GraphicsManager import *
from Entity import *

def getTileCoords(coords, tileSize):
	x = coords[0] / tileSize
	y = coords[1] / tileSize

	return (int(x), int(y))

def getNewPath(start, end):
	pass

def main():
	gameRunning = True
	tileSize = 24

	im = Image.open("map4.png", "r")
	pixels = list(im.getdata())
	myMap = Map(tileSize)
	# create a map from the image
	myMap.loadMap(pixels, im.size[0], im.size[1])

	graphicsMgr = GraphicsManager(myMap)
	myPathfinder = Pathfinder()

	path = None
	
	startCoord = (0, 0)
	endCoord = (0, 0)

	ninja = Entity("ninja")

	while(gameRunning):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseTilePos = getTileCoords(event.pos, tileSize)
				if event.button == 3:
					# set end pos
					startCoord = ninja.getTilePos()
					print "startcoord:", startCoord
					print "endcoord: ", endCoord
					endCoord = mouseTilePos
					path = myPathfinder.findPath(myMap, startCoord, endCoord)
					if( not path ):
						print "no path"
					else:
						ninja.setPath(path)
				elif event.button == 1:
					# select ninja
					pass

		ninja.update()
		graphicsMgr.render(myMap, path, ninja)

################################

if __name__ == "__main__":
	main()