# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/8 14:48
# 文件名称：alien.py
# 开发工具：PyCharm
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """创建外星人"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并确定第一个外星人的位置"""
        super(Alien, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        #加载外星人图像并获取其外接矩形
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #将外星人放在屏幕的左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #储存外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """向右或者向左移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
