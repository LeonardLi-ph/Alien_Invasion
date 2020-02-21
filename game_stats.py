# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/9 14:00
# 文件名称：game_stats.py
# 开发工具：PyCharm
class Gamestats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings, gf):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False        #让游戏一开始处于非活跃状态
        self.high_score = gf.trans_high_score()    #任何时候最高得分都不应该被重置

    def reset_stats(self):
        """初始化游戏期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit           # left是”剩下“的意思
        self.score = 0
        self.level = 1
