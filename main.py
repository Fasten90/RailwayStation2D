import pygame
from pygame.locals import *

import sys
import random
import math
from enum import Enum


pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

infoObject = pygame.display.Info()

IS_FULL_SCREEN = True
if IS_FULL_SCREEN:
    WIDTH = infoObject.current_w
    HEIGHT = infoObject.current_h
else:
    WIDTH = 640
    HEIGHT = 480

SCREEN_WIDTH = WIDTH

ACC = 0.5
FRIC = -0.12
FPS = 60

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
DARK_GREY = (50, 50, 50)


RAIL_TOP_Y = math.floor(HEIGHT/3)
TRAIN_MOVE_UPPER_Y = 40  # Because the 'rail' image
TRAIN_SPEED_X = 5
HIDE_X = -1000
HIDE_Y = -1000
POS_STATION_X_LEFT = math.floor(WIDTH/3)
POS_STATION_X_RIGHT = math.floor(2 * WIDTH/3)
STOP_TIME_SEC = 20 * FPS

CONFIG_GAME_NAME = "Vonatos"

class TrainPosition(Enum):
    TOP = 1
    BOTTOM = 2

class TrainDirection(Enum):
    RIGHT = 1
    LEFT = 2

FramePerSec = pygame.time.Clock()

if IS_FULL_SCREEN:
    DISPLAYSURF = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
else:
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))

BACKGROUND_COLOR = DARK_GREY  # TODO: Maybe in normal situation it should be WHITE ?
DISPLAYSURF.fill(DARK_GREY)

pygame.display.set_caption(CONFIG_GAME_NAME)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.rail_image = pygame.image.load("images/rail.PNG")
        #size_x, size_y = self.image.get_size()
        #self.image = pygame.transform.scale(self.image, (WIDTH, size_y))  # TODO: Don't know how to scale up an image like a texture...
        self.rect = self.rail_image.get_rect()
        self.rect.bottomleft=(0,RAIL_TOP_Y)  # Typically the center() recommended

        # Drawing Rectangle
        self.station = pygame.Surface((math.floor(WIDTH/3), math.floor(HEIGHT/4)))
        self.station.fill(GREY)

        # Bottom rail
        self.rail_rect_bot = self.rail_image.get_rect()
        self.rail_rect_bot.topleft=(0,HEIGHT-RAIL_TOP_Y)  # Typically the center() recommended

    def draw(self, surface):
        surface.blit(self.rail_image, self.rect) 
        surface.blit(self.station, (math.floor(WIDTH/3), math.floor(HEIGHT/3)))
        surface.blit(self.rail_image, self.rail_rect_bot) 


class Train(pygame.sprite.Sprite):
    def __init__(self, pos=TrainPosition.TOP, direction=TrainDirection.LEFT):
        super().__init__() 
        self.dir = direction
        self.img_locomotive = pygame.image.load("images/locomotive.PNG")
        self.img_traincar = pygame.image.load("images/train_car.PNG")
        self.rect = self.img_locomotive.get_rect()
        if pos == TrainPosition.TOP:
            self.start_pos_x = WIDTH - 2
            self.start_pos_y = RAIL_TOP_Y - TRAIN_MOVE_UPPER_Y  # TODO: Better calculation?
        elif pos == TrainPosition.BOTTOM:
            self.start_pos_x = 0
            self.start_pos_y = math.floor((HEIGHT/4)*3)  # TODO: Better calculation?
        self.rect.bottomleft = (self.start_pos_x, self.start_pos_y)
        self.size_x, self.size_y = self.img_locomotive.get_size()
        self.stop_time = 0

    def move(self):
        # Move + Always stop
        if self.dir == TrainDirection.LEFT:
            if self.rect.left > POS_STATION_X_RIGHT:
                speed = -TRAIN_SPEED_X
            elif POS_STATION_X_LEFT <= self.rect.left <= POS_STATION_X_RIGHT:
                speed = -1 * math.floor(TRAIN_SPEED_X/2)
            elif self.rect.left < POS_STATION_X_LEFT:
                speed = 0
                self.stop_time += 1
                if self.stop_time > STOP_TIME_SEC:
                    speed = -TRAIN_SPEED_X
            else:
                speed = -TRAIN_SPEED_X
        elif self.dir == TrainDirection.RIGHT:
            if self.rect.right < POS_STATION_X_LEFT:
                speed = TRAIN_SPEED_X
            elif POS_STATION_X_LEFT <= self.rect.right <= POS_STATION_X_RIGHT:
                speed = math.floor(TRAIN_SPEED_X/2)
            elif self.rect.right > POS_STATION_X_RIGHT:
                speed = 0
                self.stop_time += 1
                if self.stop_time > STOP_TIME_SEC:
                    speed = TRAIN_SPEED_X
            else:
                speed = TRAIN_SPEED_X
        self.rect.move_ip(speed, 0)
        # Check if outside of screen
        if (self.rect.right > WIDTH + self.size_x):
            self.hide()
        elif (self.rect.left < 0 - self.size_x):
            self.hide()

    def draw(self, surface):
        surface.blit(self.img_locomotive, self.rect) 

    def hide(self):
        self.rect.top = HIDE_Y
        self.rect.center = (HIDE_X, HIDE_Y)

    def re_create(self):
        self.rect.bottomleft = (self.start_pos_x, self.start_pos_y)
        self.stop_time = 0


background = Background()
train_top = Train(TrainPosition.TOP, TrainDirection.LEFT)
train_bottom = Train(TrainPosition.BOTTOM, TrainDirection.RIGHT)


def quit():
    pygame.quit()
    sys.exit()


# Game loop begins
while True:
    # Check events
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        quit()

    # Cheats
    if pressed_keys[K_RIGHT]:
        train_top.re_create()
        train_bottom.re_create()

    # Moves / refresh
    background.update()
    train_top.move()
    train_bottom.move()

    # Display / pygame administration
    DISPLAYSURF.fill(DARK_GREY)
    background.draw(DISPLAYSURF)
    train_top.draw(DISPLAYSURF)
    train_bottom.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)

