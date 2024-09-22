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

CONFIG_GAME_NAME = "Vonatos"

class TrainPosition(Enum):
    TOP = 1
    BOTTOM = 2

 
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


# images/train_car.PNG
class Train(pygame.sprite.Sprite):
    def __init__(self, pos=TrainPosition.TOP):
        super().__init__() 
        self.image = pygame.image.load("images/locomotive.PNG")
        self.rect = self.image.get_rect()
        if pos == TrainPosition.TOP:
            pos_y = RAIL_TOP_Y - TRAIN_MOVE_UPPER_Y
        elif pos == TrainPosition.BOTTOM:
            pos_y = math.floor((HEIGHT/4)*3)
        self.rect.bottomleft=(0, pos_y)
        self.size_x, self.size_y = self.image.get_size()

    def move(self):
        self.rect.move_ip(TRAIN_SPEED_X, 0)
        if (self.rect.right > WIDTH + self.size_x):
            self.rect.top = HIDE_Y
            self.rect.center = (HIDE_X, HIDE_Y)
        elif (self.rect.left < 0 - self.size_x):
            self.rect.top = HIDE_Y
            self.rect.center = (HIDE_X, HIDE_Y)

    def draw(self, surface):
        surface.blit(self.image, self.rect) 

    def re_create(self):
        self.rect.bottomleft = (0, RAIL_TOP_Y - TRAIN_MOVE_UPPER_Y)


background = Background()
train_top = Train(TrainPosition.TOP)
train_bottom = Train(TrainPosition.BOTTOM)

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

    # Normal things
    background.update()
    train_top.move()
    train_bottom.move()

    DISPLAYSURF.fill(DARK_GREY)
    background.draw(DISPLAYSURF)
    train_top.draw(DISPLAYSURF)
    train_bottom.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)

