import KBEngine
from KBEDebug import *
from Rules_DDZ import *
import random
import json

class DdzAvatar(KBEngine.Entity):

	def __init__(self):
		KBEngine.Entity.__init__(self)

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

	def onEnterGame(self,gameID,result):
		self.gameID = gameID
		self.base.reqEnterHall(1)

	def onLeaveGame(self,gameID):
		pass

	def onEnterHall(self,hallID):
		self.hallID = hallID
		self.base.reqEnterRoom("广东省深圳市")
		pass

	def onLeaveHall(self,hallID):
		pass

	def onEnterRoom(self,data):
		pass
