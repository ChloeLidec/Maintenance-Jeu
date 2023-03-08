"""Class Player"""

import pygame
import constantes as const
import bullets as bul

class Player (pygame.sprite.Sprite):
    """Classe du joueur
    Args:
        pygame.sprite.Sprite (Sprite): icone du joueur
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
        self.img_index = 0 # Player Wizard Image Index

    def shoot (self, bullet_img):
        bullet = bul.Bullet (bullet_img, self.rect.midtop)
        self.bullets.add (bullet)

    def move_up (self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.top >= const.SCREEN_HEIGHT - self.rect.height:
            self.rect.top = const.SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def move_left (self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right (self):
        if self.rect.left >= const.SCREEN_WIDTH - self.rect.width:
            self.rect.left = const.SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed
