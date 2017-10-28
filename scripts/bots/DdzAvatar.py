import KBEngine
from KBEDebug import *
from Rules_DDZ import *
import random
import json

class DdzAvatar(KBEngine.Entity):

	def __init__(self):
		KBEngine.Entity.__init__(self)

		self.chairID = 0

		self.base.reqEnterGame(1)

		DEBUG_MSG("Bots::DdzAvatar __init__")

	def onContinue(self):
		pass

	def onMessage(self,retcode,action,data):
		data_json = json.loads(data)
		if action == ACTION_ROOM_COMPUTE :
			self.base.reqContinue()

	def onSay(self,str):
		pass
