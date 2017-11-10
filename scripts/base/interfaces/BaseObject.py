import KBEngine
from KBEDebug import *

class BaseObject():
    """Base实体基类 匹配机制下如 游戏大厅，游戏房间"""

    def __init__(self):

        # 子逻辑分支，如游戏的子分支为游戏大厅，大厅的子分支为房间
        self.childs = {}

        # 玩家管理
        self.players = {}

    def reqEnter(self,player):
        """进入对应的空间，需要实体添加对该空间的引用"""

        self.players[player.id] = player

        for prop in player.propertys:
            if self.className.find(prop) != -1 and self.className != "Games":
                setattr(player,prop.lower(),self)

        DEBUG_MSG("%s[%d]::reqEnter() Entity[%d]" % (self.className,self.id,player.id))

    def reqLeave(self,player):
        """离开对应的空间，需要清空实体对该空间的引用"""

        if player.id in self.players:
            del self.players[player.id]

        for prop in player.propertys:
            if self.className.find(prop) != -1 and self.className != "Games":
                setattr(player, prop.lower(), None)

        DEBUG_MSG("%s[%d]::reqLeave() Entity[%d]" % (self.className, self.id,player.id))

    def reqEnterChild(self,player,cid):

        if cid in self.childs:
            self.childs[cid].reqEnter(player)

    def reqPlayerCount(self):
        """获取空间内玩家数量"""
        return len(self.players)
