from State import *

class State_Idle( State ):
	def __init__(self):
		State.__init__(self)

	def Enter(self, pEntity):
		print "%d: Idle" % pEntity.id

	def Execute(self, pEntity):
		pass

	def Exit(self, pEntity):
		pass