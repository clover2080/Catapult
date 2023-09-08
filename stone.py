import math
import pygame
from pygame.color import Color
from animation import Animation
from const import *

class Stone(Animation):
    def __init__(self):
        self.sprite_image = 'stone.png'
        self.sprite_width = 8
        self.sprite_height = 8
        self.sprite_columns = 4
        self.fps = 20
        self.state = STONE_READY
        self.init_animation()
        self.moveX = 10
        self.moveY = 3

    def update(self):
        self.calc_next_frame()

        rect = (self.sprite_width*self.current_frame, 0,
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0,0), rect)
        self.image.set_colorkey(Color(255, 0, 255))

    def setup(self, initial_pos, power, direction):
        self.initial_pos = initial_pos
        self.rect.x = initial_pos[0]
        self.rect.y = initial_pos[0]
        self.power = power
        self.direction = direction
        self.state = STONE_FLY

    def move(self, time, space, decrement_stones):
        pos = self.calculate_position(time, g, self.direction)

        pos = self.map_position(
            self.initial_pos[0], self.initial_pos[1],
            pos[0], pos[1])
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if pos[0] > space[0] or pos[1] > space[1]:
            self.state = STONE_READY
            decrement_stones()

    #투석 위치 계산
    def calculate_position(self, t, g, direction):
        r = math.radians(direction)
        x = self.power*math.cos(r)*t
        y = self.power*math.sin(r)*t - 0.5*g*math.pow(t, 2)

        return (int(x), int(y))

    #투석의 위치를 화면 좌표에 맞게 변환
    def map_position(self, x, y, new_x, new_y):
        return (x + new_x, y + (new_y*-1))

    def update(self):
        if self.rect.left < 0 or self.rect.right > 415:
            self.moveX = -self.moveX
        if self.rect.top < 0 or self.rect.bottom > 300:
            self.moveY = -self.moveY

        self.rect.x += self.moveX
        self.rect.y += self.moveY


    #돌 코드
