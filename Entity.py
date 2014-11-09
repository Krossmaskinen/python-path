import math

from Path import *

class Entity:
	idCounter = 0

	def __init__(self, type):
		self.setId()
		self.debug = False
		self.type = type
		self.pos = [0, 0]
		self.currentTarget = None
		self.path = None
		self.prevPath = None
		self.direction = [0.0, 0.0]
		self.speed = 0.2
		self.moving = False
		self.isSelected = False
		self.isBlocked = False

	def setId(self):
		self.id = Entity.idCounter
		Entity.idCounter += 1

	def getDirection(self, start, end):
		# normalize and return the direction
		xv = float(end[0] - start[0])
		yv = float(end[1] - start[1])

		totalLength = self.getDistance(start, end)

		if( totalLength == 0 ):
			return (0, 0)
		else:
			return (xv / totalLength, yv / totalLength)

	def getDistance(self, start, end):
		xv = abs(float(end[0] - start[0]))
		yv = abs(float(end[1] - start[1]))

		return math.sqrt(xv + yv)
	
	def setPosition(self, coords):
		if( self.currentTarget ):
			if( self.debug ): print self.currentTarget.x, self.currentTarget.y
			currentDistance = self.getDistance(self.pos, (self.currentTarget.x, self.currentTarget.y))
			newDistance = self.getDistance(coords, (self.currentTarget.x, self.currentTarget.y))

			# target is reached or passed
			if(currentDistance < newDistance):
				if( self.debug ): print "snap"
				self.pos[0], self.pos[1] = self.currentTarget.x, self.currentTarget.y
			else: 
				if( self.debug ): print "move"
				self.pos[0], self.pos[1] = coords[0], coords[1]
		else:
			if( self.debug ): print "teleport"
			self.pos[0], self.pos[1] = coords[0], coords[1]

		if( self.debug ): print "new pos %d, %d" % (self.pos[0], self.pos[1])

	def setPath(self, path):
		self.currentTarget = None
		self.path = path
		self.prevPath = Path()

	def moveAlongPath(self, pEntities = None):
		self.moving = True
		validPath = False

		if( len(self.path.nodes) > 0 ):
			validPath = True

		if( not self.currentTarget and validPath ):
			if( self.debug ): print "getting first target"
			# add the second and delete the first node (the ninja will be on the first node anyways, no need to target it first)
			self.currentTarget = self.path.nodes.pop(1)
			self.prevPath.nodes.append(self.path.nodes[0])
			del self.path.nodes[0]

		elif( validPath and self.pos[0] == self.currentTarget.x and self.pos[1] == self.currentTarget.y ):
			if( self.debug ): print "current target reached, targetting next"
			self.prevPath.nodes.append(self.currentTarget)
			self.currentTarget = self.path.nodes.pop(0)

		if( pEntities ):
			for entity in pEntities:
				if( self.id != entity.id ):
					entityPos = entity.getTilePos()
					currentPos = self.currentTarget.getTilePos()
					if( currentPos[0] == entityPos[0] and currentPos[1] == entityPos[1] ):
						self.block()

		if( not validPath ):
			if( self.debug ): print "final target reached"
			# target reached
			print "stop2"
			self.stopMoving()
			return False
		elif( not self.isBlocked ):
			if( self.debug ): print "setting direction for the next target"
			self.direction = self.getDirection( self.pos, ( self.currentTarget.x, self.currentTarget.y ) )
			self.move()


	def stopMoving(self):
		if( self.debug ): print "stop moving"
		self.path = None
		self.direction = None
		self.moving = False

	def move(self):
		if( self.debug ): print "moving"

		if( self.moving and self.direction ):
			if( self.debug ): print "moving and have direction"
			if( self.debug ): print "direction: %d, %d" % (self.direction[0], self.direction[1])
			newPos = (self.pos[0] + self.speed * self.direction[0], self.pos[1] + self.speed * self.direction[1]) 
			self.setPosition( newPos )
		else:
			print "stop1"
			self.stopMoving()

	def update(self, pMap, pPathfinder, pEntities = None):
		if( self.isBlocked ):
			print "new path"
			self.path = pPathfinder.findPath( pMap, self.getTilePos(), (self.path.nodes[-1].x, self.path.nodes[-1].y), pEntities )
			self.currentTarget = None
			self.isBlocked = False
		
		if( self.path ):
			self.moveAlongPath(pEntities)

	def getTilePos(self):
		return ( int(self.pos[0] + 0.5), int(self.pos[1] + 0.5) )

	def block(self):
		self.isBlocked = True

	def select(self):
		self.isSelected = True

	def unselect(self):
		self.isSelected = False