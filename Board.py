import copy
import random
import time
import traceback
import turtle
from math import ceil, floor

import pygame

from Algo import *
from Food import Food
from Snake import Snake

pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([600, 600])

# Run until the user asks to quit
running = True
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    QUIT,
)
class Board:
    def __init__(self, width,height,spacing):
        self.window_width = 1200
        self.window_height = 800
        self.width = width
        self.height = height
        self.spacing = spacing
        self.speed = 60
        self.fps = pygame.time.Clock()
        self.rows = (self.window_height) // (self.height  )
        self.cols = self.window_width//(self.width )
        centerx = self.cols//2
        centery = self.rows//2
        self.mode = "ai"
        self.gameover = False
        self.snake = Snake(centerx-1, centery, 15)
        self.food = Food( centerx,centery, pygame.Color(0,0,255)  )
        # self.generate_new()
        self.food.x = centerx+1
        self.food.y = centery
        self.surface = pygame.display.set_mode(size=(self.window_width, self.window_height))
        self.background_color= pygame.Color(0,0,0)
        self.boundary_color = pygame.Color(128,128,128)
        self.boundary_blocks = []
        self.init_boundary_blocks()
        screen.fill( self.background_color )
        pygame.display.flip()
        self.ind_ai = 0

    def draw_snake(self):
        for i in reversed(self.snake.segments):
            pygame.draw.rect(screen, i.color,
                             pygame.Rect(i.x*self.width, i.y*self.height, self.width-self.spacing, self.height-self.spacing))

    def draw_food(self):
        pygame.draw.rect(screen, self.food.color,
                         pygame.Rect(self.food.x * self.width, self.food.y * self.height, self.width - self.spacing,
                                     self.height - self.spacing))

    def draw_boundary(self):
        # UP
        pygame.draw.rect( screen, self.boundary_color,
                          pygame.Rect(0,0, self.window_width, self.height))


        # DOWN
        pygame.draw.rect( screen, self.boundary_color,
                          pygame.Rect(0, self.window_height- self.height, self.window_width, self.height))

        # LEFT
        pygame.draw.rect( screen, self.boundary_color,
                          pygame.Rect(0, 0,  self.width, self.window_height))

        # RIGHT
        pygame.draw.rect( screen, self.boundary_color,
                          pygame.Rect(self.window_width-self.width, 0,self.width, self.window_height))

    def draw_game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, pygame.Color( 255,255,255 ))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])

    def has_hit_boundary(self, location):
        if location[0] == 0 or location[0] == self.cols-1: return True
        elif location[1] == 0 or location[1] == self.rows-1: return True


    def generate_new(self):
        snake_positions = [ [seg.x, seg.y]  for seg  in self.snake.segments    ]
        while [self.food.x,self.food.y] in snake_positions:
            self.food.x = random.randint(1,self.cols-2)
            self.food.y = random.randint(1,self.rows-2)


    def has_reached_food(self):
        if self.snake.segments[0].x == self.food.x and self.snake.segments[0].y == self.food.y:
            self.generate_new()
            self.snake.grow()
            return True
        return False

    def get_possible_moves(self):
        prev = self.snake.delta

        blocks = [[self.snake.segments[i].x, self.snake.segments[i].y] for i in range(1, len(self.snake.segments) - 1)]
        blocks.extend(self.boundary_blocks)
        possible = []
        if not self.snake.is_up_oriented():
            #   [0,-1] might be possible
            self.snake.delta = [0, -1]
            if self.has_hit_boundary(self.snake.get_next()) or self.snake.has_hit_self(self.snake.get_next()):
                self.snake.delta = prev
            else:
                possible.append([0, -1])
            self.snake.delta = prev

        if not self.snake.is_down_oriented():
            self.snake.delta = [0, 1]
            if self.has_hit_boundary(self.snake.get_next()) or self.snake.has_hit_self(self.snake.get_next()):
                self.snake.delta = prev
            else:
                possible.append([0, 1])
            self.snake.delta = prev

        if not self.snake.is_left_oriented():
            self.snake.delta = [-1, 0]
            if self.has_hit_boundary(self.snake.get_next()) or self.snake.has_hit_self(self.snake.get_next()):
                self.snake.delta = prev
            else:
                possible.append([-1, 0])
            self.snake.delta = prev

        if not self.snake.is_right_oriented():
            self.snake.delta = [1, 0]
            if self.has_hit_boundary(self.snake.get_next()) or self.snake.has_hit_self(self.snake.get_next()):
                self.snake.delta = prev
            else:
                possible.append([1, 0])
            self.snake.delta = prev
        return possible


    def update(self):
        running = True
        moves =[]

        while running:
            snake_blocks = [[self.snake.segments[i].x, self.snake.segments[i].y] for i in
                      range(1, len(self.snake.segments) - 1)]
            possible = self.get_possible_moves()
            safe_path = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.gameover and self.mode == "human":
                        if event.key == K_UP:
                            if not self.snake.is_up_oriented():
                                self.snake.delta = [0,-1]
                        elif event.key == K_DOWN:
                            if not self.snake.is_down_oriented():
                                self.snake.delta = [0,1]
                        elif event.key == K_LEFT:
                            if not self.snake.is_left_oriented():
                                self.snake.delta = [-1,0]
                        elif event.key == K_RIGHT:
                            if not self.snake.is_right_oriented():
                                self.snake.delta = [1,0]
                    elif self.gameover and event.key == K_SPACE:
                        self.__init__(self.width, self.height, self.spacing)
                        self.update()
            try:
                if not self.gameover:
                    if moves == -1 or self.ind_ai >= len(moves) or (not safe_path):

                        head = [self.snake.segments[0].x, self.snake.segments[0].y]
                        goal = [self.food.x, self.food.y]
                        moves, safe_path = move(head,goal,snake_blocks,self.boundary_blocks,self.rows,self.cols,possible)
                        self.ind_ai = 0


                    if len(moves) != 0:
                        self.snake.delta = moves[self.ind_ai]
                        self.ind_ai += 1



            except Exception as e:
                traceback.print_exc()
                continue

            if self.has_hit_boundary(self.snake.get_next() ) or self.snake.has_hit_self():
                self.gameover = True
            # Fill the background with white
            if self.gameover:
                self.draw_game_over()
            else:
                screen.fill( self.background_color )
                self.snake.update()

                if self.has_reached_food():
                    pass
                start = time.time()
                # moves = move(head,goal,blocks, self.rows, self.cols )
                end = time.time()
                self.draw_snake()
                self.draw_food()
                self.draw_boundary()
                self.fps.tick( self.speed )
            pygame.display.flip()


    def init_boundary_blocks(self):
        self.boundary_blocks.extend(  [  [x,0] for x in range(0,self.cols+1)   ]   )
        self.boundary_blocks.extend(  [  [x,self.rows-1] for x in range(0,self.cols+1)   ]   )

        self.boundary_blocks.extend(  [  [0,x] for x in range(0,self.rows)   ]   )
        self.boundary_blocks.extend(  [  [self.cols-1,x] for x in range(0,self.rows)   ]   )