# -*- coding: utf-8 -*-
"""Airplan War Game
Developped by Tom Germain & Chloé Lidec / 23A
"""

import random
import datetime
import enemy as enem
import boss as boss
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

difficulty = 0

# Load the picture of the plane
plane_img = pygame.image.load('resources/image/shoot.png')

# Parameters of the ennemies
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
enemies_down = pygame.sprite.Group()

# Parameters of the boss
boss_rect = pygame.Rect(534, 612, 57, 43)
#the image of the boss is the same as the enemy but twice as big
boss_img = pygame.transform.scale(plane_img.subsurface(boss_rect), (114, 86))
boss_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
boss_down_sound.set_volume(const.VOLUME)
boss_down_imgs = []
boss_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
boss_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
boss_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
boss_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
boss_object = boss.Boss(boss_img, boss_down_imgs, boss_down_sound, const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
boss_group = pygame.sprite.Group()
boss_group.add(boss_object)

bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
bullet_sound.set_volume(const.VOLUME)
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)


# Parameters of the player
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126)) # Player's image zone
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126)) # Player's explosion  image zone
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


progress_bar_height = 10
progress_bar_max_value = 100
# Value of the progress bar
progress_bar_value = 0
fight_pg_value = 0

def shoot(cpt,player):
    """ Make the player shoot

    Args:
        cpt (int): cpt of the shoot
        player (Player): player object
    
    Returns:
        int: cpt of the shoot after the shoot

    """
    cpt_shoot=cpt
    if cpt_shoot % const.SHOOT_FREQUENCY == 0:
        bullet_sound.play()
        player.shoot(bullet_img)
    cpt_shoot += 1
    if cpt_shoot >= const.SHOOT_FREQUENCY:
        cpt_shoot = 0
    return cpt_shoot

def triple_shoot(player):
    """Make the player shoot 3 bullets

    Args:
        player (Player): player object
    """
    bullet_sound.play()
    if player.triple_shoot_frequency >=500:
        player.triple_shoot(bullet_img)

def move_bullets(bullets,player):
    """Move the bullets

    Args:
        bullets (list): list of bullets
        player (Player): player object
    """
    for bullet in bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

def move_boss_bullets(boss_object,player):
    """Move the boss bullets

    Args:
        boss_bullets (list): list of boss bullets
        player (Player): player object
    """
    for bullet in boss_object.bullets:
        bullet.move_boss()
        if pygame.sprite.collide_circle_ratio(0.5)(bullet, player):
            boss_object.bullets.remove(bullet)
            player.hp -= 1
            break
        if bullet.rect.top > const.SCREEN_HEIGHT:
            boss_object.bullets.remove(bullet)
def spawn_ennemies(enemies,cpt):
    """Spawn ennemies

    Args:
        enemies (list): list of ennemies
        cpt (int): cpt of the ennemies

    Returns:
        int: cpt of the ennemies after the spawn
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

def move_ennemies(ennemies,difficulty=1):
    """Move the ennemies

    Args:
        ennemies (list): list of ennemies
        difficulty (int): difficulty of the game
    """
    for enemy in ennemies:
        enemy.move(difficulty)
        # Déterminez si le player a été touché
        if pygame.sprite.collide_circle_ratio(0.5)(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > const.SCREEN_HEIGHT:
            ennemies.remove(enemy)
def ennemies_down_test(ennemies,player):
    """Test if the ennemies are down

    Args:
        ennemies (list): list of ennemies
        player (Player): player object
    """
    list_ennemies_down = pygame.sprite.groupcollide(ennemies, player.bullets, 1, 1)
    for enemy_down in list_ennemies_down:
        enemies_down.add(enemy_down)

def boss_shot_test(boss_object,player):
    """Test if the boss is shot

    Args:
        boss_object (Boss): boss object
        player (Player): player object
    """
    #test if the sprite boss is shot
    for bullet in player.bullets:
        if pygame.sprite.collide_rect(boss_object,bullet):
            boss_object.hp -= 10
            player.bullets.remove(bullet)

def down_anim(ennemies_down):
    """Animation of the ennemies down

    Args:
        ennemies_down (list): list of ennemies down

    Returns:
        int: score of the player
    """
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
    """Change the difficulty of the game

    Args:
        tuple (tuple): tuple of the difficulties
        index (int): index of the difficulty
    """
    global difficulty
    difficulty = const.DIFFICULTIES[index]

def game_function():
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
    global difficulty
    global progress_bar_value
    global progress_bar_height

    clock = pygame.time.Clock()
    running = True
    score=0
    player.reset()
    enemies1.empty()
    enemies_down.empty()
    main_menu.disable()
    main_menu.full_reset()
    while running:
        # control the game speed
        clock.tick(45)
        # Draw the background
        i = 0
        while i <tiles :
            screen.blit(background, (0,background.get_height() * i + scroll))
            i += 1
        scroll -= 1
        if abs(scroll) == background.get_height():
            scroll = 0

        # Draw the progress bar at the top of the screen
        pygame.draw.rect(screen, (0, 0, 0), (0,const.SCREEN_HEIGHT-progress_bar_height, 100, progress_bar_height))
        pygame.draw.rect(screen, (255, 200, 64), (0,const.SCREEN_HEIGHT-progress_bar_height, progress_bar_value, progress_bar_height))
        #draw a text on the right of the progress bar
        charge_font = pygame.font.Font(None, 32)
        charge_text = charge_font.render("Triple shoot charger", True, (255, 200, 64))
        text_rect = charge_text.get_rect()
        text_rect.topleft = [0, const.SCREEN_HEIGHT-progress_bar_height - 20]
        screen.blit(charge_text, text_rect)
        # Draw an airplane
        screen.blit(player.image[player.img_index], player.rect)
 
        # handle game's events
        cpt_apparition_bullet = shoot(cpt_apparition_bullet,player)
        move_bullets(player.bullets,player)
        player.bullets.draw(screen)

        cpt_apparition_enemy=spawn_ennemies(enemies1, cpt_apparition_enemy)
        move_ennemies(enemies1,difficulty)
        ennemies_down_test(enemies1,player)

        # get score
        score+=down_anim(enemies_down)
        enemies1.draw(screen)
        # draw the score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # show score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # draw the player
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            player.img_index = cpt_apparition_bullet // const.INDEX_ANIM
        else:
            player.img_index = player_down_index // const.INDEX_ANIM
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 25:# time of the animation
                running = False

        # add 0.5 to the player's triple shoot charger
        if player.triple_shoot_frequency <500:
            player.triple_shoot_frequency += 1
            #the pg value is the percentage of the triple shoot charger
            progress_bar_value = player.triple_shoot_frequency / 5
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
        if key_pressed[lo.K_SPACE]:
            triple_shoot(player)
        # Process game exits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    game_over_menu("infinite")

def game_fight_mode():
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
    global difficulty
    global progress_bar_value
    global progress_bar_height
    global fight_pg_value

    clock = pygame.time.Clock()
    running = True
    score=0
    fight_pg_value = 0
    player.reset()
    boss_object.reset()
    enemies1.empty()
    enemies_down.empty()
    main_menu.disable()
    main_menu.full_reset()
    while running:
        # control the game speed
        clock.tick(45)
        # Draw the background
        i = 0
        while i <tiles :
            screen.blit(background, (0,background.get_height() * i + scroll))
            i += 1
        scroll -= 1
        if abs(scroll) == background.get_height():
            scroll = 0
        # Draw the progress bar at the bottom of the screen
        pygame.draw.rect(screen, (0, 0, 0), (0,const.SCREEN_HEIGHT-progress_bar_height-20, 100, progress_bar_height))
        pygame.draw.rect(screen, (255, 200, 64), (0,const.SCREEN_HEIGHT-progress_bar_height-20, progress_bar_value, progress_bar_height))
        #draw a text on the right of the progress bar
        charge_font = pygame.font.Font(None, 32)
        charge_text = charge_font.render("Triple shoot charger", True, (255, 200, 64))
        text_rect = charge_text.get_rect()
        text_rect.topleft = [0, const.SCREEN_HEIGHT-progress_bar_height - 40]
        screen.blit(charge_text, text_rect)

        # Draw the progress bar at the top of the screen
        pygame.draw.rect(screen, (0, 0, 0), (0,const.SCREEN_HEIGHT-progress_bar_height, const.SCREEN_WIDTH, progress_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (0,0, fight_pg_value, progress_bar_height))
        #draw a text on the right of the progress bar
        charge_font = pygame.font.Font(None, 32)
        charge_text = charge_font.render("Road to boss", True, (0, 255, 0))
        text_rect = charge_text.get_rect()
        text_rect.topleft = [0, 20]
        screen.blit(charge_text, text_rect)
        # Draw an airplane
        screen.blit(player.image[player.img_index], player.rect)
 
        # handle game's events
        cpt_apparition_bullet = shoot(cpt_apparition_bullet,player)
        move_bullets(player.bullets,player)
        player.bullets.draw(screen)

        cpt_apparition_enemy=spawn_ennemies(enemies1, cpt_apparition_enemy)
        move_ennemies(enemies1,difficulty)
        ennemies_down_test(enemies1,player)

        # get score
        score+=down_anim(enemies_down)
        fight_pg_value = score / 50 *0.48
        enemies1.draw(screen)
        # draw the score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # show score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # draw the player
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            player.img_index = cpt_apparition_bullet // const.INDEX_ANIM
        else:
            player.img_index = player_down_index // const.INDEX_ANIM
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 25:# time of the animation
                running = False

        # add 0.5 to the player's triple shoot charger
        if player.triple_shoot_frequency <500:
            player.triple_shoot_frequency += 1
            #the pg value is the percentage of the triple shoot charger
            progress_bar_value = player.triple_shoot_frequency / 5
        # Update the screen
        if fight_pg_value >= const.SCREEN_WIDTH:
            boss_battle()
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
        if key_pressed[lo.K_SPACE]:
            triple_shoot(player)
        

        # Process game exits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    game_over_menu("fight")

def boss_battle():
    global score
    global boss_object
    global boss_bullets
    global main_menu
    global scroll
    global player
    global cpt_apparition_bullet
    global cpt_apparition_enemy
    global player_down_index
    global game_over
    global game_over_sound
    global bullet_sound
    global bullet_img
    global enemy1_down_sound
    global enemies1
    global enemies_down
    global score
    global difficulty
    global progress_bar_value
    global progress_bar_height
    global fight_pg_value

    clock = pygame.time.Clock()
    running = True
    player.reset()
    enemies1.empty()
    enemies_down.empty()
    start_time = datetime.datetime.now()
    while running:
        # control the game speed
        clock.tick(45)
        # Draw the background
        i = 0
        while i <tiles :
            screen.blit(background, (0,background.get_height() * i + scroll))
            i += 1
        scroll -= 1
        if abs(scroll) == background.get_height():
            scroll = 0

        #draw the boss
        boss_group.draw(screen)
        #draw the boss bullets
        
        i = random.randint(0, 60)
        if i == 1:
            boss_object.shoot(bullet_img)
        elif i == 2:
            boss_object.spawn_ennemies(enemies1,enemy1_img, enemy1_down_imgs, enemy1_rect)
        move_ennemies(enemies1,difficulty)
        ennemies_down_test(enemies1,player)

        move_boss_bullets(boss_object,player)
        # Draw the progress bar at the bottom of the screen
        pygame.draw.rect(screen, (0, 0, 0), (0,const.SCREEN_HEIGHT-progress_bar_height-20, 100, progress_bar_height))
        pygame.draw.rect(screen, (255, 200, 64), (0,const.SCREEN_HEIGHT-progress_bar_height-20, progress_bar_value, progress_bar_height))
        #draw a text on the right of the progress bar
        charge_font = pygame.font.Font(None, 32)
        charge_text = charge_font.render("Triple shoot charger", True, (255, 200, 64))
        text_rect = charge_text.get_rect()
        text_rect.topleft = [0, const.SCREEN_HEIGHT-progress_bar_height - 40]
        screen.blit(charge_text, text_rect)

        # Draw the progress bar at the top of the screen
        pygame.draw.rect(screen, (0, 0, 0), (0,0, const.SCREEN_WIDTH, progress_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (0,0, (boss_object.hp/5)*4.8 , progress_bar_height))
        #draw a text on the right of the progress bar
        charge_font = pygame.font.Font(None, 32)
        charge_text = charge_font.render("Boss life", True, (0, 255, 0))
        text_rect = charge_text.get_rect()
        text_rect.topleft = [0, 20]
        screen.blit(charge_text, text_rect)

        # Draw the progress bar at the top of the screen
        pygame.draw.rect(screen, (0, 0, 0), (0,const.SCREEN_HEIGHT-progress_bar_height - 60, const.SCREEN_WIDTH, progress_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (0,const.SCREEN_HEIGHT-progress_bar_height - 60, (player.hp*10)*4.8 , progress_bar_height))
        #draw a text on the right of the progress bar
        charge_font = pygame.font.Font(None, 32)
        charge_text = charge_font.render("Your life", True, (0, 255, 0))
        text_rect = charge_text.get_rect()
        text_rect.topleft = [0, const.SCREEN_HEIGHT-progress_bar_height - 80]
        screen.blit(charge_text, text_rect)

        # Draw an airplane
        screen.blit(player.image[player.img_index], player.rect)
 
        # handle game's events
        cpt_apparition_bullet = shoot(cpt_apparition_bullet,player)
        move_bullets(player.bullets,player)
        player.bullets.draw(screen)
        boss_shot_test(boss_object,player)
        # get score
        enemies1.draw(screen)
        boss_object.bullets.draw(screen)
        # draw the player
        if not player.is_hit and player.hp > 0:
            screen.blit(player.image[player.img_index], player.rect)
            player.img_index = cpt_apparition_bullet // const.INDEX_ANIM
        else:
            player.img_index = player_down_index // const.INDEX_ANIM
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 25:# time of the animation
                running = False

        # add 0.5 to the player's triple shoot charger
        if player.triple_shoot_frequency <500:
            player.triple_shoot_frequency += 1
            #the pg value is the percentage of the triple shoot charger
            progress_bar_value = player.triple_shoot_frequency / 5
        # Update the screen

        if boss_object.hp <= 0:
            running = False
            game_over_menu("win",start_time)
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
        if key_pressed[lo.K_SPACE]:
            triple_shoot(player)
        

        # Process game exits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    game_over_menu("lose",start_time)

def game_over_menu(mode,start_time=0):
    surface = create_example_window("Airplane war", (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    
    if mode == "win":
        theme = pygame_menu.themes.THEME_GREEN.copy()
        theme.set_background_color_opacity(0.5)
        menu = pygame_menu.Menu(
            height = const.SCREEN_HEIGHT,
            title = 'You won',
            theme = theme,
            width = const.SCREEN_WIDTH)
        menu.add.label('Time: '+ str(datetime.datetime.now() - start_time) + 's')
        menu.add.button('Play again',game_fight_mode)
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
    elif mode == "lose":
        theme = pygame_menu.themes.THEME_ORANGE.copy()
        theme.set_background_color_opacity(0.5)
        menu = pygame_menu.Menu(
            height = const.SCREEN_HEIGHT,
            title = 'You lost',
            theme = theme,
            width = const.SCREEN_WIDTH)
        menu.add.label('Time: '+ str(datetime.datetime.now() - start_time) + 's')
        menu.add.button('Play again',game_fight_mode)
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
    else:
        theme = pygame_menu.themes.THEME_ORANGE.copy()
        theme.set_background_color_opacity(0.5)
        theme.background_color = (pygame_menu.BaseImage(image_path=const.GAME_OVER))
        menu = pygame_menu.Menu(
            height = const.SCREEN_HEIGHT,
            title = 'Game Over',
            theme = theme,
            width = const.SCREEN_WIDTH)
        menu.add.label('Score: '+ str(score))
        if mode == "fight":
            menu.add.button('Play again',game_fight_mode)
        else:
            menu.add.button('Play again',game_function)
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
    global difficulty

    surface = create_example_window("Airplane war", (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    theme = pygame_menu.themes.THEME_DARK.copy()
    
    play_menu = pygame_menu.Menu(
        height = const.SCREEN_HEIGHT,
        title = 'Launch a game',
        theme = theme,
        width = const.SCREEN_WIDTH)
    play_menu.add.button('Play', game_function)
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
    main_menu.add.button('Play infinite mode', play_menu)
    main_menu.add.button('Play fight mode', game_fight_mode)
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
    