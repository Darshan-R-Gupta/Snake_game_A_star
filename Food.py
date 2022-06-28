import random

import pygame

class Food:
    def __init__(self, x,y , color=pygame.Color( 255,0,0 ) ):
        self.color = color
        self.x = x
        self.y = y
        self.eaten = False

    def update(self):
        if self.eaten:
            self.eaten = False
