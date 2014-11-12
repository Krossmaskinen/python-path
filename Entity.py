import math

from Path import *
import Globals

class Entity:
	idCounter = 0
	_pathfinder = None

	def __init__(self, type, pPathfinder):
		self.setId()
		self.debug = False
		self.type = type
		self.pos = [0, 0]
		self.prevPos = []
		self.prevTile = []
		self.currentTarget = None
		self.path = None
		self.prevPath = None
		self.direction = [0.0, 0.0]
		self.speed = 0.2
		self.moving = False
		self.isSelected = False
		self.isBlocked = False
		self.currentState = None

		if( not self._pathfinder ):
			self._pathfinder = pPathfinder

		self.ChangeState(Globals.gStates["Idle"])

	def setId(self):
		self.id = Entity.idCounter
		Entity.idCounter += 1

	def ChangeState(self, pNewState):
		if( self.currentState ):
			self.currentState.Exit(self)
		self.currentState = pNewState
		self.currentState.Enter(self)

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
		if( coords ):
			if( not self.isBlocked and self.currentTarget ):
				currentDistance = self.getDistance(self.pos, (self.currentTarget.pos[0], self.currentTarget.pos[1]))
				newDistance = self.getDistance(coords, (self.currentTarget.pos[0], self.currentTarget.pos[1]))

				# target is reached or passed
				if(currentDistance < newDistance):
					self.pos[0], self.pos[1] = self.currentTarget.pos[0], self.currentTarget.pos[1]
				else: 
					if( self.debug ): print "%d: move" % self.id
					self.pos[0], self.pos[1] = coords[0], coords[1]
			else:
				if( self.debug ): print "%d: teleport" % self.id
				self.pos[0], self.pos[1] = coords[0], coords[1]

			if( self.debug ): print "%d: after set position %d, %d" % (self.id, self.pos[0], self.pos[1])

	def setPath(self, path):
		print "%d: setting path" % self.id
		self.currentTarget = None
		self.path = path
		self.prevPath = Path()

	def moveAlongPath(self):
		validPath = False

		if( len(self.path.nodes) > 0 ):
			validPath = True

		if( not self.currentTarget and validPath ):
			if( self.debug ): print "getting first target"
			# add the second and delete the first node (the ninja will be on the first node anyways, no need to target it first)
			self.currentTarget = self.path.nodes.pop(1)
			self.prevPath.nodes.append(self.path.nodes[0])
			del self.path.nodes[0]


		elif( validPath and self.pos[0] == self.currentTarget.pos[0] and self.pos[1] == self.currentTarget.pos[1] ):
			if( self.debug ): print "current target reached, targetting next"
			self.prevPath.nodes.append(self.currentTarget)
			self.currentTarget = self.path.nodes.pop(0)

		if( Globals.gEntities ):
			for entity in Globals.gEntities:
				if( self.id != entity.id ):
					entityPos = entity.getTilePos()
					currentPos = self.currentTarget.getTilePos()
					if( currentPos[0] == entityPos[0] and currentPos[1] == entityPos[1] ):
						# self.ChangeState(Globals.gStates["Blocked"])
						self.isBlocked = True
					else:
						self.moving = True
		else:
			self.moving = True

		if( not validPath ):
			if( self.debug ):
				print "final target reached"
				print "stop2"
			# target reached
			self.stopMoving()
			return False
		elif( not self.isBlocked ):
			if( self.debug ): print "setting direction for the next target"
			self.direction = self.getDirection( self.pos, ( self.currentTarget.pos[0], self.currentTarget.pos[1] ) )
			self.move()
			return True

		return True


	def stopMoving(self):
		if( self.debug ): print "stop moving"
		# self.path = None
		self.direction = None
		self.moving = False

	def move(self):
		if( self.debug ): print "moving"
		self.moving = True

		if( self.moving and self.direction ):
			self.prevPos = self.pos

			tileBeforeMove = self.getTilePos()

			# set prev tile

			if( self.debug ): print "moving and have direction"
			if( self.debug ): print "direction: %d, %d" % (self.direction[0], self.direction[1])
			newPos = (self.pos[0] + self.speed * self.direction[0], self.pos[1] + self.speed * self.direction[1]) 
			self.setPosition( newPos )

			currentTile = self.getTilePos()
			if( not self.prevTile ):
				self.prevTile = tileBeforeMove
			elif( self.prevTile and ( tileBeforeMove[0] == currentTile[0] and tileBeforeMove[1] == currentTile[1] ) ):
				pass
			else:
				self.prevTile = tileBeforeMove
		else:
			if( self.debug ): print "stop1"
			self.stopMoving()

	def update(self):
		self.currentState.Execute(self)

		# if(self.debug): print "id: %d" % self.id
		# if( self.isBlocked and self.path ):
		# 	if( self.debug ): print "new path"
		# 	# find a new way from the current position to the target
		# 	if(self.path):
		# 		print len(self.path.nodes)

		# 		for node in self.path.nodes:
		# 			print "%d, %d" % (node.pos[0], node.pos[1])
		# 	else:
		# 		print "why no nodes?"
		# 	# bulle = raw_input(">")
		# 	self.path = pPathfinder.findPath( pMap, self.getTilePos(), (self.path.nodes[-1].pos[0], self.path.nodes[-1].pos[1]), Globals.gEntities )
		# elif( self.isBlocked and not self.path ):
		# 	self.stopMoving()
		# 	self.setPosition( self.prevTile )
		# else:
		# 	self.isBlocked = False
		
		# if( self.path ):
		# 	self.moveAlongPath(Globals.gEntities)

	def getTilePos(self):
		return ( int(round(self.pos[0])), int(round(self.pos[1])) )

	def select(self):
		self.isSelected = True

	def unselect(self):
		self.isSelected = False
