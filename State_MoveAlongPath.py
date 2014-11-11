from State import *
import Globals

class State_MoveAlongPath( State ):
	def __init__(self):
		State.__init__(self)

	def Enter(self, pEntity):
		print "%d: following path" % pEntity.id
		print "start: " % pEntity.path.nodes[0]
		print "end: " % pEntity.path.nodes[-1]

	def Execute(self, pEntity):
		if( pEntity.path ):
			if( not pEntity.moveAlongPath() ):
				pEntity.ChangeState(Globals.gStates["Idle"])	
		else:
			pEntity.ChangeState(Globals.gStates["Idle"])

	def Exit(self, pEntity):
		print "%d: stopped following path" % pEntity.id