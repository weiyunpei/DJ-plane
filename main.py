import random
import sys
import traceback

import my_plane
import pygame
import enemy
import bullet
import supply
from pygame.locals import *

pygame.init()
pygame.mixer.init()

SCREEN_RECT = pygame.Rect(0, 0, 513, 720)
# 游戏的帧率
ZHENLV = 60

# 补给发放时间
SUPPLY_TIME = USEREVENT

# 超级子弹
DOUBLE_BULLET_TIME = USEREVENT + 1

# 解除我方无敌状态计时器
INVINCIBLE_TIME = USEREVENT + 2

bg_size = width, height = SCREEN_RECT.size
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战 -- 牧")

# 导入背景
background = pygame.image.load("./image/litang.png").convert()

game_over_ground = pygame.image.load("./image/gameoverbackground.png")

# 颜色参数
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 载入游戏音乐
pygame.mixer.music.load("./sound/zood.mp3")
pygame.mixer.music.set_volume(0.1)

bomb_sound = pygame.mixer.Sound("./sound/xuebaobizui.wav")
bomb_sound.set_volume(0.7)
supply_sound = pygame.mixer.Sound("./sound/achievement.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("./sound/zhishixuebao.wav")
get_bomb_sound.set_volume(0.3)
get_bullet_sound = pygame.mixer.Sound("./sound/mamashengde.wav")
get_bullet_sound.set_volume(0.5)
upgrade_sound = pygame.mixer.Sound("./sound/BGM.wav")
upgrade_sound.set_volume(0)
enemy3_fly_sound = pygame.mixer.Sound("./sound/button.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("./sound/enemy0_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("./sound/enemy1_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("./sound/enemy2_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("./sound/wocenimenma.wav")
me_down_sound.set_volume(0.4)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)

    # 生成我方飞机
    me = my_plane.Myplane(bg_size)

    # 生成敌方飞机
    enemies = pygame.sprite.Group()

    # 生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    # 发射频率
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0

    # 发射频率
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    clock = pygame.time.Clock()

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font("./font/字魂50号-白鸽天行体.ttf", 36)

    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("./image/game_pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("./image/game_pause_pressed.png").convert_alpha()

    resume_nor_image = pygame.image.load("./image/game_resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("./image/game_resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # 难度系数
    level = score // 400
    level1 = level

    # 每过一定分奖励一个炸弹
    bomb = 0
    bomb1 = bomb

    # 全屏炸弹
    bomb_image = pygame.image.load("./image/xuebao.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("./font/字魂50号-白鸽天行体.ttf", 48)
    bomb_num = 3

    # 每30s发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    # SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # 超级子弹
    # DOUBLE_BULLET_TIME = USEREVENT + 1

    # 解除我方无敌状态计时器
    # INVINCIBLE_TIME = USEREVENT + 2

    # 标志是否使用超级子弹
    is_double_bullet = False

    # 生命数量
    life_image = pygame.image.load("./image/icon1.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 用于阻止重复打开记录文件
    recorded = False

    # 游戏结束画面
    gameover_font = pygame.font.Font("./font/字魂50号-白鸽天行体.ttf", 48)
    again_image = pygame.image.load("./image/restart_sel.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("./image/quit_sel.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 用于切换图片
    switch_image = True

    # 用于延迟
    delay = 100

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                if paused:
                    pygame.time.set_timer(SUPPLY_TIME, 0)
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                else:
                    pygame.time.set_timer(SUPPLY_TIME, 20 * 1000)
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if random.randint(0, 1):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # 根据用户的得分上难度
        level = score // 400
        bomb = (score * level) // 1000
        if level1 != level:
            upgrade_sound.play()
            # 增加三架小型敌机，两架中级，一架大型
            add_small_enemies(small_enemies, enemies, level + 2)
            add_mid_enemies(mid_enemies, enemies, level + 1)
            add_big_enemies(big_enemies, enemies, level)
            # 提升小型敌机的速度
            inc_speed(small_enemies, level // 5)
            # 提升中级敌机的速度
            inc_speed(mid_enemies, level // 10)
            # 提升大型敌机的速度
            inc_speed(big_enemies, level // 20)
            level1 = level
        if bomb1 != bomb:
            bomb_num += 1
            bomb1 = bomb

        screen.blit(background, (0, 0))

        if life_num and not paused:

            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w]:
                me.move_up()
            elif key_pressed[K_s]:
                me.move_down()
            elif key_pressed[K_a]:
                me.move_left()
            elif key_pressed[K_d]:
                me.move_right()

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 10:
                        bomb_num += 1
                    bomb_supply.active = False

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    # 发射超级子弹
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bomb_supply.active = False

            # 发射子弹
            if not (delay % 10):

                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        # 绘制被打到的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 画血条
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)

                    # 当生命大于20显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                    # 即将出现在画面中，播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play()
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (1 + e3_destroy_index) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 100
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    # 毁灭
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 画血条
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)

                    # 当生命大于20显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                else:
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (1 + e2_destroy_index) % 4
                        if e2_destroy_index == 0:
                            score += 50
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    # 毁灭
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (1 + e1_destroy_index) % 4
                        if e1_destroy_index == 0:
                            score += 10
                            each.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                me_down_sound.play()
                if not (delay % 3):
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (1 + me_destroy_index) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render("× %d" % bomb_num, True, BLACK)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width,
                                             height - 10 - life_rect.height))

            # 绘制得分
            score_text = score_font.render("Score: %s" % str(score), True, BLACK)
            screen.blit(score_text, (10, 5))

        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()

            # 停止全部音效
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded = True
                # 读取历史最高分
                with open("./record.txt", "r") as f:
                    record_score = int(f.read())

                # 如果玩家最高分高于历史得分，存档
                if score > record_score:
                    with open("./record.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束界面
            screen.blit(game_over_ground, (0, 0))

            # 绘制结束画面
            record_score_text = score_font.render("Best : %d" % record_score, True, BLACK)
            screen.blit(record_score_text, (5, 0))

            gameover_text1 = gameover_font.render("Your Score", True, BLACK)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, \
                                                                (height // 2) - 100 - gameover_text1_rect.height
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, BLACK)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (((width - gameover_text2_rect.width) // 2),
                                                                 gameover_text1_rect.bottom + 10)
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = (width - again_rect.width) // 2, again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)


            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击重新开始
                if again_rect.left < pos[0] < again_rect.right \
                        and again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数重新开始
                    main()
                # 如果用户点击结束游戏
                elif gameover_rect.left < pos[0] < gameover_rect.right \
                        and gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 切换图片
        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()

        clock.tick(ZHENLV)


if __name__ == '__main__':
    try:
        main()

    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
