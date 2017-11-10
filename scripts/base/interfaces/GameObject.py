# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class GameObject:
    """
    服务端非房卡游戏对象的基础接口类
    """
    def __init__(self):

        #基类属性数组
        self.propertys = ["Game","Hall","Room"]

        #代理引用
        self.activeProxy = None

        #转化为小写后动态生成类属性
        for prop in self.propertys:
            setattr(self,prop.lower(),None)

    def Games(self):

        return KBEngine.globalData.get("Games")

    def ExitGame(self):
        """清空所有引用,才能在服务器上销毁该实体"""

        self.reqLeaveRoom()
        self.reqLeaveHall()
        self.reqLeaveGame()
        self.Games().reqLeave(self)

        DEBUG_MSG("%r[%d]::ExitGame()" % (self.className,self.id))

    def reqEnterGame(self,cid):

        self.Games().reqEnterChild(self,cid)

    def reqLeaveGame(self):

        if self.game:
            self.game.reqLeave(self)

    def reqEnterHall(self,cid):

        if self.game:
            self.game.reqEnterChild(self,cid)

    def reqLeaveHall(self):

        if self.hall:
            self.hall.reqLeave(self)

    def reqEnterRoom(self):

        if self.hall:
            self.hall.reqEnterChild(self)

    def reqLeaveRoom(self):

        if self.room:
            self.room.reqLeave(self)


