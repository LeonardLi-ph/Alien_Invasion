# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/6 21:03
# 文件名称：alien_invasion.py
# 开发工具：PyCharm
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard

def run_game():
    """初始化游戏并且创建一个屏幕"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    play_button = Button(ai_settings, screen, "Play")
    ship = Ship(ai_settings, screen)     #创建一艘飞船
    alien = Alien(ai_settings, screen)   #创建一个外星人
    bullets = Group()                    #为子弹创建一个编组
    aliens = Group()                     #为外星人创建一个编组

    gf.create_fleet(ai_settings, screen, ship, aliens)    #创建外星人群
    #创建储存游戏统计信息的实例，并且创建记分牌
    stats = Gamestats(ai_settings, gf)
    sb = Scoreboard(ai_settings, screen, stats)

    #开始游戏的主循环系统
    while True:
        gf.check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)      #监视键盘和鼠标
        if stats.game_active:        #飞船还有生命值时才会运行
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button,sb)

run_game()