from PIL import Image
from Map import *
from Node import *
from Path import *
from Pathfinder import *

def main():
	im = Image.open("map3.png", "r")
	pixels = list(im.getdata())
	myMap = Map()
	# create a map from the image
	myMap.loadMap(pixels, im.size[0], im.size[1])

	myPathfinder = Pathfinder()
	
	oldStart = (0, 0)
	oldEnd = (im.size[0] - 1, im.size[1] - 1)

	path = myPathfinder.findPath(myMap, oldStart, oldEnd)
	closedPath = Path()
	closedPath.nodes = myPathfinder.closedList;

	myMap.printMapWithPath(path)
	myMap.printMapWithPath(closedPath)

################################

main()