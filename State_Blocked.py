from State import *

import Globals

class State_Blocked( State ):
	def __init__(self):
		State.__init__(self)

	def Enter(self, pEntity):
		print "%d: Blocked" % pEntity.id
		print "%d: prev tile: " % pEntity.id, pEntity.prevTile
		pEntity.isBlocked = True
		# #move to clear tile
		pEntity.setPosition( pEntity.prevTile )

		print "%d: new pos: " % pEntity.id, pEntity.getTilePos()

	def Execute(self, pEntity):
		# find a new path if possible
		print "%d: get tile pos: " % pEntity.id, pEntity.getTilePos()
		path = pEntity._pathfinder.findPath(pEntity.getTilePos(), pEntity.path.nodes[-1].pos)
		if( path ):
			print "%d: path found!" % pEntity.id
			pEntity.ChangeState( Globals.gStates["MoveAlongPath"] )
		else:
			print "%d: no path available, still blocked" % pEntity.id

	def Exit(self, pEntity):
		print "%d: Unblocked" % pEntity.id
		pEntity.isBlocked = False