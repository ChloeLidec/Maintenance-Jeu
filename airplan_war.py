# -*- coding: utf-8 -*-
"""Airplan War Game
Developped by Tom Germain & Chloé Lidec / 23A
"""

import random
import enemy as enem
from sys import exit
import pygame
import pygame.locals as lo
import constantes as const
import player as pl
import math
import pygame_menu
from pygame_menu.examples import create_example_window
# Initialize the game
pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display. set_caption('Airplane Wars')
# Background
background = pygame.image.load('resources/image/background.png').convert()
scroll = 0
tiles = math.ceil(const.SCREEN_HEIGHT / background.get_height()) + 1

difficulte = 0

# Load the picture of the plane
plane_img = pygame.image.load('resources/image/shoot.png')

# Définir les paramètres liés à la surface utilisés par l'objet avion ennemi
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemies1 = pygame.sprite.Group()
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
enemy1_down_sound.set_volume(const.VOLUME)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
cpt_apparition_enemy = 0
# Stockez des avions détruits pour le rendu d'animations de sprites d'épaves
enemies_down = pygame.sprite.Group()


bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
bullet_sound.set_volume(const.VOLUME)
#Définir les paramètres liés à la surface utilisés par l'objet puce(bullets)
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# Définir les paramètres liés au joueur
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126)) # Zone d'image du sprite du joueur
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126)) # Zone d'image du sprite d'explosion du joueur
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = pl.Player(plane_img, player_rect, player_pos)
cpt_apparition_bullet = 0
player_down_index = 16

game_over = pygame.image.load('resources/image/gameover.png')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
game_over_sound.set_volume(const.VOLUME)


def tirs(compteur,joueur):
    """Fait tirer le joueur

    Arguments:
        compteur {int} -- Compteur des tirs
        player {Player} -- Objet joueur


    Returns:
        int -- Compteur des tirs après le tir
    """
    cpt_tirs=compteur
    if cpt_tirs % const.SHOOT_FREQUENCY == 0:
        bullet_sound.play()
        joueur.shoot(bullet_img)
    cpt_tirs += 1
    if cpt_tirs >= const.SHOOT_FREQUENCY:
        cpt_tirs = 0
    return cpt_tirs
def deplacer_puces(bullets,joueur):
    """Déplace les puce vers le haut

    Arguments:
        bullets {list} -- Liste des puce
        player {Player} -- Objet joueur"""
    for bullet in bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            joueur.bullets.remove(bullet)

def faire_apparaitre_ennemies(enemies,cpt):
    """Fait apparaitre des ennemies

        Arguments:
            enemies {list} -- Liste des ennemies
            cpt {int} --compteur des ennemies

        Returns:
            int -- Compteur des ennemies aprèes l'apparition
        """
    cpt_ennemis=cpt
    if cpt_ennemis % const.ENEMY_FREQUENCY == 0:
        enemy1_pos = [random.randint(0, const.SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = enem.Enemy(enemy1_img,
                    enemy1_down_imgs,
                    enemy1_pos)
        enemies.add(enemy1)
    cpt_ennemis += 1
    if cpt_ennemis >= const.ENEMY_FREQUENCY:
        cpt_ennemis = 0
    return cpt_ennemis

def deplacer_ennemies(ennemies):
    """Déplace les ennemies vers le bas et les enleves si ils sortent de l'écran

        Arguments:
            ennemies {list} -- Liste des ennemies"""
    for enemy in ennemies:
        enemy.move()
        # Déterminez si le joueur a été touché
        if pygame.sprite.collide_circle_ratio(0.5)(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > const.SCREEN_HEIGHT:
            ennemies.remove(enemy)
def ennemies_touche(ennemies,joueur):
    """Vérifie si les ennemies sont touchés par les puce et les enlève si c'est le cas

    Arguments:
        ennemies {list} -- Liste des ennemies
        player {Player} -- Objet joueur
    """
    enemiesa_down = pygame.sprite.groupcollide(ennemies, joueur.bullets, 1, 1)
    for enemy_down in enemiesa_down:
        enemies_down.add(enemy_down)

def epaves(ennemies_down):
    """Gère les animations des épaves

    Arguments:
        ennemies_down {list} -- Liste des épaves

        Returns:
            score {int} -- Score du joueur recupéré des épaves"""
    score_act=0
    for enemy_down in ennemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)

            score_act += 1000

            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1
    return score_act

def change_difficulty(tuple,index):
    """Change la difficulté du jeu

    Arguments:
        values {tuple} -- Valeur de la difficulté"""
    global difficulte
    difficulte = const.DIFFICULTIES[index]
    print(difficulte)

def fonction_jeu():
    global main_menu
    global scroll
    global player
    global cpt_apparition_bullet
    global cpt_apparition_enemy
    global player_down_index
    global game_over
    global game_over_sound
    global bullet_sound
    global enemy1_down_sound
    global enemies1
    global enemies_down
    global score
    global difficulte
    print(difficulte)
    clock = pygame.time.Clock()
    running = True
    score=0

    main_menu.disable()
    main_menu.full_reset()
    while running:
        # Contrôlez la fréquence d'images maximale du jeu
        clock.tick(45)
        # Draw the background
        i = 0
        while i <tiles :
            screen.blit(background, (0,background.get_height() * i + scroll))
            i += 1
        scroll -= 1
        if abs(scroll) == background.get_height():
            scroll = 0
        # Draw an airplane
        screen.blit(player.image[player.img_index], player.rect)
 
        # Gérer les événements
        cpt_apparition_bullet = tirs(cpt_apparition_bullet,player)
        deplacer_puces(player.bullets,player)
        player.bullets.draw(screen)

        cpt_apparition_enemy=faire_apparaitre_ennemies(enemies1, cpt_apparition_enemy)
        deplacer_ennemies(enemies1)
        ennemies_touche(enemies1,player)

        # Dessinez l'animation de l'épave
        score+=epaves(enemies_down)
        enemies1.draw(screen)
        # dessiner le score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # dessiner le score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # dessiner l'avion du joueur
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            # Changer l'index de l'image pour animer l'avion
            player.img_index = cpt_apparition_bullet // const.INDEX_ANIM
        else:
            player.img_index = player_down_index // const.INDEX_ANIM
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 25:#gere le temps de l'animation de l'avion
                running = False

        # Update the screen
        pygame.display.update()
        key_pressed = pygame.key.get_pressed()
        if key_pressed[lo.K_w] or key_pressed[lo.K_UP]:
            player.move_up()
        if key_pressed[lo.K_s] or key_pressed[lo.K_DOWN]:
            player.move_down()
        if key_pressed[lo.K_a] or key_pressed[lo.K_LEFT]:
            player.move_left()
        if key_pressed[lo.K_d] or key_pressed[lo.K_RIGHT]:
            player.move_right()

        # Process game exits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    game_over_menu()


def game_over_menu():
    surface = create_example_window("Airplane war", (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    
    theme = pygame_menu.themes.THEME_ORANGE.copy()
    theme.set_background_color_opacity(0.5)
    theme.background_color = (pygame_menu.BaseImage(image_path=const.GAME_OVER))
    menu = pygame_menu.Menu(
        height = const.SCREEN_HEIGHT,
        title = 'Game Over',
        theme = theme,
        width = const.SCREEN_WIDTH)
    menu.add.label('Score: '+ str(score))
    menu.add.button('Play again', fonction_jeu)
    menu.add.button('Return to main menu', main)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.add.vertical_margin(500)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        menu.update(events)
        menu.draw(surface)
        pygame.display.flip()

def main():
    global main_menu
    global surface
    global difficulte

    surface = create_example_window("Airplane war", (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    theme = pygame_menu.themes.THEME_DARK.copy()
    
    play_menu = pygame_menu.Menu(
        height = const.SCREEN_HEIGHT,
        title = 'Launch a game',
        theme = theme,
        width = const.SCREEN_WIDTH)
    play_menu.add.button('Play', fonction_jeu)
    play_menu.add.selector('Difficulty :', [('Easy', 0), ('Medium', 1),('Hard',2)], onchange=change_difficulty, selector_id='diff')
    play_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    commands_menu = pygame_menu.Menu(
        height = const.SCREEN_HEIGHT,
        theme = theme,
        title = 'Commands',
        width = const.SCREEN_WIDTH
    )
    commands_menu.add.label('Move :  ^  \n           <  v  >')
    commands_menu.add.label('Triple shoot : Space')
    commands_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    main_menu = pygame_menu.Menu(
        height = const.SCREEN_HEIGHT,
        title = 'Airplane War',
        theme = theme,
        width = const.SCREEN_WIDTH
    )
    main_menu.add.button('Play', play_menu)
    main_menu.add.button('Commands', commands_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        #paint bg
        screen.blit(background, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if main_menu.is_enabled():
            main_menu.update(events)
            main_menu.draw(surface)
        
        pygame.display.update()

if __name__ == '__main__':
    main()
    