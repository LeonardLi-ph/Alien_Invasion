# _*_ coding:utf-8 _*_
# 开发人员：Leonard Li
# 开发时间：2020/2/7 14:19
# 文件名称：game_functions.py
# 开发工具：PyCharm
import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship,aliens, bullets, stats, sb):
    """检查按键按下的情况"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_KP_ENTER:
        game_begin_settings(ai_settings, screen, ship, aliens, bullets, stats, sb)


def check_keyup_events(event, ship):
    """检查按键松开的情况"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb):
    """响应按键和鼠标"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #检测是否关闭窗口
            sys.exit()

        elif event.type == pygame.KEYDOWN:      #检测按键（左右）按下时会有什么反应
            check_keydown_events(event, ai_settings, screen, ship,aliens, bullets, stats, sb)

        elif event.type == pygame.KEYUP:        #检测按键（左右）松开时会有什么反应
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN  :      #检测鼠标点击是否在'Play'按钮中
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y, sb)

def check_play_button(ai_settings, screen, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y, sb):
    """在玩家单击按钮时游戏开始"""
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:
        game_begin_settings(ai_settings, screen, ship, aliens, bullets, stats, sb)

def game_begin_settings(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """重置游戏设置"""
    ai_settings.initialize_dynamic_settings()  # 重置游戏设置
    pygame.mouse.set_visible(False)            # 隐藏光标
    stats.reset_stats()                        # 重置游戏统计信息
    stats.game_active = True                   # 激活游戏

    # 重置游戏得分、最高得分、等级
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()

    # 清空外星人和子弹
    aliens.empty()
    bullets.empty()

    # 创建一群外星人并使其居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button,sb):
    """更新屏幕并且把图片加载到屏幕上"""
    screen.fill(ai_settings.bg_color)    # 每次循环都重新绘制屏幕
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()                       #绘制飞船
    aliens.draw(screen)                 #绘制外星人
    sb.show_score()                     #显示得分
    sb.prep_ships()                     #显示飞船编组

    #如果游戏处于非活动状态就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()                # 让最近绘制的屏幕可见

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """更新子弹的位置，并删除已经消失的子弹"""
    #更新子弹的位置
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb)

def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """检查子弹和外星人的碰撞"""
    #检查是否有子弹击中了外星人，如果有，则删除子弹和外星人!!! (这函数真厉害)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #删除现有的子弹并且加快游戏速度
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1         #提高等级
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)     #重新创建一群外星人,

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没达到限制，就发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)  # 创建一颗新子弹
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """获取外星人的数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并且放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #创建一个外星人并计算一行可以容纳多少个外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并且加入到当前编组行中
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移并且更新整群外星人的位置"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检查是否有外星人位于屏幕边缘，更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    #检查是否有外星人碰到屏幕底部
    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """响应被外星人撞到的飞船"""
    stats.ships_left -= 1            #飞船（生命值）减一
    sb.prep_ships()                  #更新计分牌

    if stats.ships_left > 0:
        #清空外星人和所有子弹
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人并且把飞船重新放置到屏幕中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)          #暂停0.5s
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检查飞船是否到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #和外星人撞到飞船类似
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def check_high_score(stats, sb):
    """检查是否出现了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        store_high_score(stats)

def store_high_score(stats):
    """储存最高分数到文件中"""
    filename = r'high_score.txt'
    with open(filename, 'w') as file_object:
        str_high_score = str(stats.high_score)
        file_object.write(str_high_score)

def trans_high_score():
    """从文件中调用最高分数"""
    global transfer_high_score
    filename = r'high_score.txt'
    with open(filename, 'r') as file_object:
        for line in file_object:
            str_high_score = line.rstrip()
            transfer_high_score = int(str_high_score)
    return transfer_high_score













