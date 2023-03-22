"""Classe enemy"""

import pygame
import math
import constantes as const

class Enemy(pygame.sprite.Sprite):
    """_summary_ : Enemy plane deplacement

    Args:
        pygame (_type_): pygame
    """
    def __init__(self, enemy_img, enemy_down_imgs,init_pos):
        """_summary_ : Enemy plane initialization

        Args:
            enemy_img (_type_): Enemy plane image
            init_pos (_type_): Enemy plane initial position
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 5
        self.down_index = 0

    def move (self,difficulty):
        """_summary_ : Enemy plane movement
        """
        self.rect.top += self.speed +(0.8 * difficulty)
        if difficulty == 3:
            self.rect.left += math.sin(self.rect.top/100)*5
            if self.rect.left > const.SCREEN_WIDTH:
                self.rect.left = 0
