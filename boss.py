"""Classe enemy"""

import pygame
import bullets as bul
import enemy as enem
import constantes as const
import random

class Boss(pygame.sprite.Sprite):
    """_summary_ : Enemy plane deplacement

    Args:
        pygame (_type_): pygame
    """
    def __init__(self,boss_img, boss_down_imgs, boss_down_sound, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.rect.topleft = [screen_width/2 - 50, 0]
        self.down_imgs = boss_down_imgs
        self.down_sound = boss_down_sound
        self.speed = 2
        self.down_index = 0
        self.hp = 500
        self.bullets = pygame.sprite.Group()
    
    def spawn_ennemies(self,enemies,enemy1_img, enemy1_down_imgs, enemy1_rect):
        """ make 3 enemies spawn """
        for i in range(3):
            enemy1_pos = [random.randint(0, const.SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = enem.Enemy(enemy1_img,
                        enemy1_down_imgs,
                        enemy1_pos)
            enemies.add(enemy1)

    def shoot(self, bullet_img):
        bullet = bul.Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)
    
    def reset(self):
        self.rect.topleft = [const.SCREEN_WIDTH/2 - 50, 0]
        self.down_index = 0
        self.hp = 500
        self.bullets = pygame.sprite.Group()