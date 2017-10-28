# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import Helper

class DdzAvatar(KBEngine.Proxy):
    """
    斗地主房间内玩家实体
    """
    def __init__(self):
        KBEngine.Proxy.__init__(self)

        self.activePlayer = None
        self.bContinue = False

    def onEntitiesEnabled(self):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        INFO_MSG("DdzAvatar[%i-%s] entities enable. spaceUTypeB=%s, mailbox:%s" % (
        self.id, self.nameB, self.spaceUTypeB, self.client))

    def createCell(self, space, cid):
        """
        defined method.
        """
        if not self.cell:

            self.cellData["nameC"] = self.name
            self.cellData["goldC"] = self.gold
            self.cellData["sexC"]  = self.sex
            self.cellData["headC"] = self.head
            self.cellData["addrC"] = self.addr
            self.cellData["cards"] = []
            self.cellData["cardCount"] = 0
            self.cellData["curScore"]  = -1
            self.cellData["showCards"] = []
            self.cellData["multiple"] = 1
            self.cellData["type"] = 0  # 0无身份 1地主 2农民
            self.cellData["tuoguan"] = 0  # 0正常 1托管
            self.cellData["cid"] = cid

            self.createCellEntity(space)

            self.bContinue = False

    def onGetCell(self):
        """
        KBEngine method.
        entity的cell部分实体被创建成功
        """
        DEBUG_MSG('Avatar::onGetCell: %s' % self.cell)

    def onLoseCell(self):
        """
        KBEngine method.
        """
        DEBUG_MSG("%s::onLoseCell: %r" % (self.className, self.id))

        if self.bContinue:
            self.reqEnterRoom(self.addr)

        elif not self.client:
            self.destroy()

    def destroySelf(self):
        pass

    def onClientDeath(self):

        if self.state == 0:
            if self.cell:
                self.destroyCellEntity()
            else:
                self.destroy()

    def reqMessage(self, action, string):
        """
        exposed
        """
        KBEngine.globalData["Halls" + str(self.gameID)].reqMessage(self, action, string)

    def set_gold(self, settleGold):

        gold = Helper.Round(settleGold)
        self.gold += gold

        DEBUG_MSG("DdzAvatar::set_gold avatar[%r] self.gold[%r] settleGold[%r]" % (self.id, self.gold, gold))
