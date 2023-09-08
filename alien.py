import pygame
import sys
from pygame.locals import *
from pygame.color import Color
from animation import Animation
from const import *

class Alien(Animation):
    def __init__(self):
        self.sprite_image = 'alien.png'
        self.sprite_width = 32
        self.sprite_height = 32
        self.sprite_columns = 3
        self.fps = 10
        self.init_animation()
        self.moveX = 10
        self.moveY = 3
        
    def update(self):
        self.calc_next_frame()

        rect = (self.sprite_width*self.current_frame, 0,
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0, 0), rect)
        self.image.set_colorkey(Color(255, 0, 255))

        if self.rect.left < 0 or self.rect.right > 400:
            self.moveX = -self.moveX
        if self.rect.top < 0 or self.rect.bottom > 300:
            self.moveY = -self.moveY
            
        self.rect.x += self.moveX
        self.rect.y += self.moveY
'''
        if self.rect.right > BASE_Y or self.rect.x < 0:
            self.rect.x -= 5
        if self.rect.right > BASE_Y or self.rect.y < 0:
            self.rect.y -= 10

        '''
        
        #외계인 코드
