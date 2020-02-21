# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/9 17:31
# 文件名称：scoreboard.py
# 开发工具：PyCharm
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """显示得分信息"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及到的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #显示的得分时的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 40)

        self.prep_score()             #准备初始得分图像
        self.prep_high_score()        #准备最高得分图像
        self.prep_level()             #准备游戏等级
        self.prep_ships()             #显示飞船编组

    def prep_score(self):
        """将得分转化为一张图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        score_str_txt = 'Score  ' + score_str
        self.score_image = self.font.render(score_str_txt, True,
                            self.text_color, self.ai_settings.bg_color)

        #将得分放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转化为图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        high_score_str_txt = 'HighScore  ' + high_score_str
        self.high_score_image = self.font.render(high_score_str_txt, True,
                                self.text_color, self.ai_settings.bg_color)

        #将最高得分放在屏幕中间
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
         """把游戏等级转化为图像"""
         level_txt = 'Level  ' + str(self.stats.level)
         self.level_image = self.font.render(level_txt, True,
                            self.text_color, self.ai_settings.bg_color)

         #将等级放在得分的下面
         self.level_rect = self.level_image.get_rect()
         self.level_rect.right = self.score_rect.right
         self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """创建飞船编组"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示各种图案"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)



