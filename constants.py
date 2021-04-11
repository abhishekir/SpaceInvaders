import pygame

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 50)
BACKGROUND_IMG_LOC = "media/background.png"
BACKGROUND_IMG = pygame.image.load(BACKGROUND_IMG_LOC)
BACKGROUND_MUSIC_LOC = "media/background.wav"

GAME_CAPTION = "Space Invaders"
GAME_ICON = "media/game_icon.png"

PLAYER_IMAGE_LOC = "media/player.png"
PLAYER_IMG = pygame.image.load(PLAYER_IMAGE_LOC)
PLAYER_IMG_WIDTH = PLAYER_IMG.get_width()
PLAYER_IMG_HEIGHT = PLAYER_IMG.get_height()
PLAYER_X_INIT = (SCREEN_WIDTH / 2) - (PLAYER_IMG_WIDTH / 2)  # half on screen x-axis
PLAYER_Y_INIT = (SCREEN_HEIGHT * .8) + (PLAYER_IMG_HEIGHT / 2)  # 3/4 down on screen y-axis
PLAYER_VELOCITY = 4 # pixels per tick
PLAYER_BULLET_INTERVAL = 300 # milliseconds between firing a bullet

ENEMY_IMG_LOC = "media/alien.png"
ENEMY_DEATH_SOUND_LOC = "media/explosion.wav"
ENEMY_IMG = pygame.image.load(ENEMY_IMG_LOC)
ENEMY_IMG_WIDTH = ENEMY_IMG.get_width()
ENEMY_IMG_HEIGHT = ENEMY_IMG.get_height()
ENEMY_X_VELOCITY = 1.25 # pixels per tick
ENEMY_Y_VELOCITY = .2 # pixels per tick

BULLET_IMG_LOC = "media/bullet.png"
BULLET_FIRE_SOUND_LOC = "media/laser.wav"
BULLET_IMG = pygame.image.load(BULLET_IMG_LOC)
BULLET_IMG_WIDTH = BULLET_IMG.get_width()
BULLET_IMG_HEIGHT = BULLET_IMG.get_height()
BULLET_VELOCITY = 6

SCORE_FONT_SIZE = int(SCREEN_WIDTH * .05)
SCORE_FONT_COLOR = (255, 255, 255)
# SCORE_FONT = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)
SCORE_TEXT_POS = (int(SCREEN_WIDTH * .0125), int(SCREEN_HEIGHT * .0125))

import point
import random
import enemy
import bullet
import player
from pygame import mixer
