# -*- coding: utf-8 -*-

import KBEngine
from interfaces.GameObject import *
from KBEDebug import *
import Helper

class DdzAvatar(KBEngine.Proxy,GameObject):
    """
    斗地主游戏实体
    """
    def __init__(self):
        KBEngine.Proxy.__init__(self)
        GameObject.__init__(self)

        self.bContinue = False

    def onEntitiesEnabled(self):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        INFO_MSG("DdzAvatar[%i]::onEntitiesEnabled:entities enable. mailbox:%s, clientType(%i), clientDatas=(%s)" % \
            (self.id, self.client, self.getClientType(), self.getClientDatas()))

    def createCell(self, space, cid):
        """
        defined method.
        """
        if not self.cell:

            self.cellData["cards"] = []
            self.cellData["cardCount"] = 0
            self.cellData["curScore"]  = -1
            self.cellData["showCards"] = []
            self.cellData["multiple"] = 1
            self.cellData["type"] = 0       # 0无身份 1地主 2农民
            self.cellData["tuoguan"] = 0    # 0正常 1托管
            self.cellData["cid"] = cid

            self.createCellEntity(space)

            self.bContinue = False

    def onLoseCell(self):
        """
        KBEngine method.
        """
        DEBUG_MSG("%r[%r]::onLoseCell()" % (self.className, self.id))

        if self.bContinue:
            self.reqEnterRoom()

        elif not self.client:
            self.destroy()

        else:
            self.reqLeaveRoom()

    def onClientDeath(self):

        if self.state == 0:
            if self.cell:
                self.destroyCellEntity()
            else:
                self.destroy()

    def onDestroy(self):

        DEBUG_MSG("%r[%r]::onDestroy() " %(self.className,self.id))

        # 先退出大厅，退出大厅功能中应该能确保后续所有的事情
        if self.state == 0:
            self.ExitGame()

            if not self.client and self.activeProxy:
                self.activeProxy.destroy()

    def reqLeaveGame(self):

        super().reqLeaveGame()

        if self.client and self.activeProxy:

            self.giveClientTo(self.activeProxy)
            self.activeProxy.reqLeaveGame()
            self.destroy()

    def reqContinue(self):
        """
        exposed
        继续游戏
        """
        INFO_MSG("%r[%r]::reqContinue()" % (self.className,self.id))

        KBEngine.globalData["Halls" + str(self.gameID)].reqContinue(self, self.hallID, self.roomID)

    def set_gold(self, settleGold):

        gold = Helper.Round(settleGold)
        self.activeProxy.gold += gold
        self.gold = self.activeProxy.gold

        DEBUG_MSG("DdzAvatar::set_gold avatar[%r] self.gold[%r] settleGold[%r]" % (self.id, self.gold, gold))
