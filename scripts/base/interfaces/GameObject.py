# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class GameObject:
    """
    服务端非房卡游戏对象的基础接口类
    """
    def __init__(self):
        pass

    def onLoseCell(self):
        """
        KBEngine method.
        entity的cell部分实体丢失
        """
        DEBUG_MSG("%s::onLoseCell: %i" % (self.getScriptName(), self.id))

    def getGames(self):

        return KBEngine.globalData.get("Games")

    def getGame(self):

        return KBEngine.globalData.get("Game")


