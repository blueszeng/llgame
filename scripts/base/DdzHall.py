
# -*- coding: utf-8 -*-
import KBEngine
from d_config import *
from KBEDebug import *
from GlobalConst import *
from interfaces.BaseObject import *

FIND_ROOM_NOT_FOUND = 0
FIND_ROOM_CREATING = 1

class DdzHall(KBEngine.Base,BaseObject):
	"""
	大厅实体
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		BaseObject.__init__(self)

		self.lastNewRoomKey = 0

	def reqEnter(self,player):

		if player.gold < d_DDZ[self.cid]["limit"]:

			DEBUG_MSG("%r::reqEnter() Entity[%r] Gold < Limit" % (self.className, player.id))
			if player.client:
				player.client.onEnterHall(-1)
			return

		super().reqEnter(player)
		if player.client:
			player.client.onEnterHall(0)

	def reqLeave(self,player):
		super().reqLeave(player)

		if player.client:
			player.client.onLeaveHall(0)

	def onRoomGetCell(self, roomMailbox, roomID):
		"""
        Room的cell创建好了
        """
		self.childs[roomID]["roomMailbox"] = roomMailbox

		# space已经创建好了， 现在可以将之前请求进入的玩家全部丢到cell地图中
		for player in self.childs[roomID]["players"]:
			if player.client:
				roomMailbox.reqEnter(player)
			else:
				del self.childs[roomID]["players"][player]

	def onRoomLoseCell(self,roomMailbox,roomID):
		"""
		Room 销毁时，通知Hall对其进行删除
		"""
		if roomID in self.childs:
			del self.childs[roomID]

	def reqEnterRoom(self, player):
		"""
		先查找空房间，如果没空房，则将玩家排队，然后创建新房间
		"""
		for roomData in self.childs:
			if len(roomData["players"]) < 3 and roomData["mailbox"].state == ROOM_STATE_READY:
				roomData["mailbox"].reqEnter(player)
				return

		self.lastNewRoomKey = self.lastNewRoomKey + 1

		params = {"cid": self.lastNewRoomKey,
				  "parent": self,
				  "state": 0,
				  "difen": d_DDZ[self.hallID]["base"],
				  "taxRate": d_DDZ["taxRate"]}

		KBEngine.createBaseAnywhere("DdzRoom", params, None)

		roomDatas = {"mailbox": None,
					 "players": [player]}

		self.childs[self.lastNewRoomKey] = roomDatas

	def reqContinue(self,player,roomID):

		if player.gold < d_DDZ[self.hallID]["limit"]:

			DEBUG_MSG("DdzHall::reqContinue Player[%d] gold[%r] < limit[%r]" % (player.id,player.gold,d_DDZ[self.hallID]["limit"]))
			self.reqLeaveRoom(player,roomID)
			return

		DEBUG_MSG("DdzHall::reqContinue Player[%r] Hall[%r] RoomID[%r]" % (player.id, self.hallID, roomID))
		roomDatas = self.findRoom(roomID, False)

		if type(roomDatas) is dict:
			roomMailbox = roomDatas["roomMailbox"]
			if roomMailbox.state != ROOM_STATE_INGAME:

				roomMailbox.onContinue(player)

				if player.id in roomDatas["players"]:
					del roomDatas["players"][player.id]
					if len(roomDatas["players"]) <= 0:
						del self.childs[roomID]



