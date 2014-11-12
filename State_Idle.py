from State import *

class State_Idle( State ):
	def __init__(self):
		State.__init__(self)

	def Enter(self, pEntity):
		print "%d: is now idle" % pEntity.id

	def Execute(self, pEntity):
		pass

	def Exit(self, pEntity):
		print "%d: stopped being idle" % pEntity.id
		pass