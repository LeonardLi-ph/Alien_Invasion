# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/6 21:21
# 文件名称：ship.py
# 开发工具：PyCharm
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船"""

    def __init__(self,ai_settings,screen):
        """初始化飞船并确定其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将飞船放在屏幕的底部中间
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中储存小数值
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志移动飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right :     #控制飞船向右的活动范围
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left :        #控制飞船向左的活动范围
            self.center -= self.ai_settings.ship_speed_factor

        # 更新rect对象，虽然位置有所失真（self.rect.center只能储存整数值），但是影响不大
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
