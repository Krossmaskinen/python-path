from State import *

import Globals

class State_Blocked( State ):
	def __init__(self):
		State.__init__(self)

	def Enter(self, pEntity):
		print "%d: Blocked" % pEntity.id
		print "%d: prev tile: " % pEntity.id, pEntity.prevTile
		# #move to clear tile
		pEntity.setPosition( pEntity.prevTile )

		print "%d: new pos: " % pEntity.id, pEntity.getTilePos()

	def Execute(self, pEntity):
		# find a new path if possible
		pass

	def Exit(self, pEntity):
		print "%d: Unblocked" % pEntity.id