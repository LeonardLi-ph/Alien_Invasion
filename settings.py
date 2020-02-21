# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/6 21:04
# 文件名称：settings.py
# 开发工具：PyCharm
class Settings():
    """储存《外星人入侵》的所有设置类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        self.screen_width = 1280
        self.screen_height = 660
        self.bg_color = (230, 230, 230)       #颜色为RGB格式（255,255,255）=（红，绿，蓝）

        # 飞船数量（生命值）
        self.ship_limit = 3
        #子弹参数的设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        #外星人的参数
        self.fleet_drop_speed = 10
        #以什么速度加快游戏进程
        self.speedup_scale = 1.1
        #外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进程进行而变化的量"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_points = 50              #计分

        #fleet_direction为1表示右移，为-1表示左移
        self.fleet_direction = 1

    def increase_speed(self):
        """提高游戏速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)
        print(self.alien_points)

