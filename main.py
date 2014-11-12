from PIL import Image
import sys
import pygame
import time

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
	myPathfinder = Pathfinder(myMap)

	path = None
	
	startCoord = (0, 0)
	endCoord = (0, 0)

	ninja1 = Entity("ninja", myPathfinder)
	ninja2 = Entity("ninja", myPathfinder)
	ninja1.setPosition((0, 6))
	ninja2.setPosition((5, 0))


	ninjas = [ninja1, ninja2]

	Globals.gEntities = [ninja1, ninja2]

	ninja1.setPath( myPathfinder.findPath( ninja1.getTilePos(), (9, 0) ) )
	ninja2.setPath( myPathfinder.findPath( ninja2.getTilePos(), (2, 10) ) )
	ninja1.ChangeState(Globals.gStates["MoveAlongPath"])
	ninja2.ChangeState(Globals.gStates["MoveAlongPath"])

	selectedNinja = ninja1
	ninja1.select()

	Globals.gDeltaTime = time.clock() - Globals.gDeltaTime

	while(gameRunning):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseTilePos = getTileCoords(event.pos, Globals.gTileSize)
				if event.button == 3:
					# set end pos
					startCoord = selectedNinja.getTilePos()
					endCoord = mouseTilePos
					path = myPathfinder.findPath(startCoord, endCoord)
					if( not path ):
						print "no path"
					else:
						selectedNinja.setPath(path)
						selectedNinja.ChangeState(Globals.gStates["MoveAlongPath"])
				elif event.button == 1:
					print "mouse coord: ", mouseTilePos
					# select ninja
					for ninja in ninjas:
						ninja.unselect()
						ninjaPos = ninja.getTilePos()
						if ninjaPos[0] == mouseTilePos[0] and ninjaPos[1] == mouseTilePos[1]:
							selectedNinja = ninja
							ninja.select()

		for ninja in ninjas:
			ninja.update()

		graphicsMgr.render(myMap, path, ninjas)

################################

if __name__ == "__main__":
	main()