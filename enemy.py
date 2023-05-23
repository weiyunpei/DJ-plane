import pygame
from random import *


class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./image/huanghelou1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("./image/huanghelou_down_1.png").convert_alpha(),
                                    pygame.image.load("./image/huanghelou_down_2.png").convert_alpha(),
                                    pygame.image.load("./image/huanghelou_down_3.png").convert_alpha(),
                                    pygame.image.load("./image/enemy0_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        # 飞机的状态
        self.active = True

        # 设置mask检测
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width)), \
                                        (randint(-5 * self.height, 0))

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width)), \
                                        (randint(-5 * self.height, 0))


class MidEnemy(pygame.sprite.Sprite):

    energy = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./image/zhonghua1.png").convert_alpha()
        self.image_hit = pygame.image.load("./image/zhonghua1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("./image/zhonghua1_down_1.png").convert_alpha(),
                                    pygame.image.load("./image/zhonghua1_down_2.png").convert_alpha(),
                                    pygame.image.load("./image/zhonghua1_down_3.png").convert_alpha(),
                                    pygame.image.load("./image/enemy1_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True

        # 设置mask检测
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width)), \
                                        (randint(-10 * self.height, -self.height))

        self.energy = MidEnemy.energy

        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width)), \
                                        (randint(-10 * self.height, -self.height))


class BigEnemy(pygame.sprite.Sprite):

    energy = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./image/wang2.png").convert_alpha()
        self.image_hit = pygame.image.load("./image/wang2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("./image/wang2_down_1.png").convert_alpha(),
                                    pygame.image.load("./image/wang2_down_2.png").convert_alpha(),
                                    pygame.image.load("./image/wang2_down_3.png").convert_alpha(),
                                    pygame.image.load("./image/wang2_down_4.png").convert_alpha(),
                                    pygame.image.load("./image/wang2_down_5.png").convert_alpha(),
                                    pygame.image.load("./image/wang2_down_6.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        # 飞机的状态
        self.active = True

        # 设置mask检测
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width)), \
                                        (randint(-15 * self.height, -5 * self.height))

        self.energy = BigEnemy.energy

        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width)), \
                                        (randint(-15 * self.height, -5 * self.height))
