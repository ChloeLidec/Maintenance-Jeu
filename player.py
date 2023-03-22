"""Class Player"""

import pygame
import constantes as const
import bullets as bul

class Player (pygame.sprite.Sprite):
    """Class of player
    Args:
        pygame.sprite.Sprite (Sprite): player's sprite
    """
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = [] # List of pictures of player object wizard
        self.img_index = 0 # Player Wizard Image Index
        self.is_hit = False # Is the player hit?
        self.bullets = pygame.sprite.Group() # Collection of bullets fired by the player's aircraft


        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())

        self.rect = player_rect[0] # Initialize the rectangle where the picture is located
        self.rect.topleft = init_pos # Initialize the upper left corner coordinates of the rectangle
        self.speed = 8 # Initialize the player speed, here is a definite value.
        self.bullets = pygame.sprite.Group() # Collection of bullets fired by the player's aircraft
        self.triple_shoot_frequency = 0
        self.img_index = 0 # Player Wizard Image Index

    def shoot (self, bullet_img):
        bullet = bul.Bullet (bullet_img, self.rect.midtop)
        self.bullets.add (bullet)

    def triple_shoot (self, bullet_img):
        bullet1 = bul.Bullet (bullet_img, (self.rect.left + 120, self.rect.top))
        bullet2 = bul.Bullet (bullet_img, self.rect.midtop)
        bullet3 = bul.Bullet (bullet_img, (self.rect.right - 120, self.rect.top))
        self.bullets.add (bullet1, bullet2, bullet3)
        self.triple_shoot_frequency = 0

    def move_up (self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed + (const.PLAYER_SPEED *0.5)

    def move_down(self):
        if self.rect.top >= const.SCREEN_HEIGHT - self.rect.height:
            self.rect.top = const.SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed + (const.PLAYER_SPEED *0.5)

    def move_left (self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right (self):
        if self.rect.left >= const.SCREEN_WIDTH - self.rect.width:
            self.rect.left = const.SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed + (const.PLAYER_SPEED *0.5)
    def reset (self):
        self.is_hit = False
        self.img_index = 0
        self.triple_shoot_frequency = 0
        self.rect.topleft = [200, 600]
