from PIL import Image
import sys
import pygame

import Globals

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

	im = Image.open("graphics/map4.png", "r")
	pixels = list(im.getdata())
	myMap = Map(Globals.gTileSize)
	# create a map from the image
	myMap.loadMap(pixels, im.size[0], im.size[1])

	graphicsMgr = GraphicsManager(myMap)
	myPathfinder = Pathfinder()

	path = None
	
	startCoord = (0, 0)
	endCoord = (0, 0)

	ninja1 = Entity("ninja")
	ninja2 = Entity("ninja")
	ninja1.setPosition((0, 11))
	ninja2.setPosition((7, 0))

	ninjas = [ninja1, ninja2]

	Globals.gEntities = [ninja1, ninja2]

	selectedNinja = ninja1
	ninja1.select()

	while(gameRunning):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseTilePos = getTileCoords(event.pos, Globals.gTileSize)
				print "mouse pos: ", mouseTilePos
				print "ninja pos: ", selectedNinja.getTilePos()
				if event.button == 3:
					# set end pos
					startCoord = selectedNinja.getTilePos()
					endCoord = mouseTilePos
					path = myPathfinder.findPath(myMap, startCoord, endCoord)
					if( not path ):
						print "no path"
					else:
						selectedNinja.setPath(path)
						selectedNinja.ChangeState(Globals.gStates["MoveAlongPath"])
				elif event.button == 1:
					# select ninja
					for ninja in ninjas:
						ninja.unselect()
						ninjaPos = ninja.getTilePos()
						if ninjaPos[0] == mouseTilePos[0] and ninjaPos[1] == mouseTilePos[1]:
							selectedNinja = ninja
							ninja.select()

		for ninja in ninjas:
			ninja.update(myMap, myPathfinder)

		graphicsMgr.render(myMap, path, ninjas)

################################

if __name__ == "__main__":
	main()