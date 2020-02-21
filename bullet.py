# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/7 16:52
# 文件名称：bullet.py
# 开发工具：PyCharm
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """对飞船发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()        #等同于 super().__init__()
        self.screen = screen

        #在（0,0）处创建子弹的形状然后调整正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #储存用小数表示子弹的位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        self.y -= self.speed_factor         #更新表示子弹位置的小数值
        self.rect.y = self.y                #更新子弹的位置

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)



