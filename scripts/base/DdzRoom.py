# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from GlobalConst import *
from interfaces.BaseObject import *

class DdzRoom(KBEngine.Base,BaseObject):
    """
	这是一个游戏房间
	该房间中记录了房间里所有玩家的mailbox，通过mailbox我们可以将信息推送到他们的客户端。
	"""
    def __init__(self):
        KBEngine.Base.__init__(self)
        BaseObject.__init__(self)

        self.cellData["difenC"]         = self.difen
        self.cellData["taxRateC"]       = self.taxRate
        self.cellData["stateC"]         = self.state

        self.createInNewSpace(None)

    def set_state(self,state):

        if state == ROOM_STATE_READY:
            #如果将房间恢复为准备状态，即设置为结束状态，不允许再次使用
            self.state = ROOM_STATE_FINISH
        else:
            self.state = state

        for pp in self.players.values():
            pp.state = state

            #游戏结束，玩家链接不存在，则直接销毁玩家实体
            if self.state == ROOM_STATE_FINISH and not pp.client and pp.cell:
                pp.destroyCellEntity()

    def onLoseCell(self):
        """
        KBEngine method.
        entity的cell部分实体丢失
        """
        DEBUG_MSG("%r[%r]::onLoseCell()" % (self.className, self.cid))

        self.parent.onRoomLoseCell(self, self.cid)
        self.destroy()

    def onGetCell(self):
        """
        KBEngine method.
        entity的cell部分实体被创建成功
        """
        DEBUG_MSG("%r[%r]::onGetCell()" % (self.className,self.cid))

        self.parent.onRoomGetCell(self,self.cid)

    def reqEnter(self, player):
        super().reqEnter(player)

        if player.id in self.players:
            return

        if self.state == 0:

            for i in range(1, 4):
                has = False
                for pp in self.players.values():
                    if i == pp.cid:
                        has = True
                        break
                if has == False:
                    player.cid = i
                    break

            player.createCell(self.cell, player.cid)

            #满足开始游戏人数，设置玩家和房间状态1
            if len(self.players) == 3:

                self.set_state(ROOM_STATE_INGAME)
                self.cell.set_state(ROOM_STATE_INGAME)

    def reqLeave(self,player):

        #如果房间正在游戏中，不予处理
        if self.state == ROOM_STATE_INGAME:
            return

        super().reqLeave(player)

        if player.cell:
            player.destroyCellEntity()

        if self.reqPlayerCount() == 0 and self.cell:
            self.destroyCellEntity()

    def onContinue(self, player):
        DEBUG_MSG("DdzRoom::onContinue Player[%r] PlayerCount[%r]" % (player.id, len(self.players)))
        #防止多次离开
        if player.id not in self.players:
            return

        if player.cell:
            if player.id in self.players:

                del self.players[player.id]

                if player.client:
                    player.bContinue = True
                    player.client.onContinue()

            player.destroyCellEntity()

            if len(self.players) == 0 and self.cell and self.state == ROOM_STATE_FINISH:
                self.destroyCellEntity()
