import KBEngine
from KBEDebug import *

class BaseObject():
    """Base实体 匹配机制下的房间基类"""

    def __init__(self):

        # 子逻辑分支，如游戏的子分支为游戏大厅，大厅的子分支为房间
        self.childs = {}

        #玩家管理
        self.players = {}

    def reqEnter(self,player):

        self.players[player.id] = player

    def reqLeave(self,player):

        if player.id in self.players:
            del self.players[player.id]

    def reqPlayersCount(self):

        return len(self.players)
