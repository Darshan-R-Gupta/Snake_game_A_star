import turtle

import pygame


class Segment:
    def __init__(self,x, y, color =pygame.Color(0,0,255)):
        self.color= color
        self.x = x
        self.y = y


class Snake:
    def __init__(self,x,y, nseg=1,  head_color = pygame.Color(255,255,255), body_color=pygame.Color(255,255,0)):
        self.segments = []
        self.body_color = body_color
        self.head_color = head_color
        self.delta = [0,0]
        self.segments.append( Segment(x,y, self.head_color) )
        for i in range(1,nseg+1):
            self.segments.append( Segment( x, y-i, pygame.Color(255-i,255,0) )     )


    def is_up_oriented(self):
        return (self.segments[1].x == self.segments[0].x) and \
               (self.segments[1].y - self.segments[0].y <0 )

    def is_down_oriented(self):
        return (self.segments[1].x == self.segments[0].x) and \
               (self.segments[1].y - self.segments[0].y >0 )

    def is_left_oriented(self):
        return (self.segments[1].x - self.segments[0].x < 0) and \
               (self.segments[1].y == self.segments[0].y )

    def is_right_oriented(self):
        return (self.segments[1].x - self.segments[0].x > 0) and \
               (self.segments[1].y == self.segments[0].y )

    def get_next(self):
        return [self.segments[0].x + self.delta[0], self.segments[0].y + self.delta[1] ]


    def update(self):
        if self.delta == [0,0]: return
        for i in range(len(self.segments)-1,0, -1  ) :
            self.segments[i].x = self.segments[i-1].x
            self.segments[i].y = self.segments[i-1].y

        self.segments[0].x += self.delta[0]
        self.segments[0].y += self.delta[1]


    def grow(self):
        last = self.segments[-1]
        x,y = 0,0
        if self.is_up_oriented():
            x = last.x
            y = last.y-1
        elif self.is_down_oriented():
            x = last.x
            y = last.y+1
        elif self.is_left_oriented():
            x = last.x-1
            y = last.y
        else:
            x = last.x+1
            y = last.y
        col = max( 255-len(self.segments), 0 )
        self.segments.append(Segment(x,y, pygame.Color( col, 255,0 ) ))

    def has_hit_self(self,loc = None):
        if loc is None:
            head= [self.segments[0].x, self.segments[0].y]
        else:
            head = loc

        for i in range( 1, len(self.segments)-1 ):
            if head[0] == self.segments[i].x and head[1] == self.segments[i].y:
                return True
        return False

    def is_in_loc(self, loc):
        for i in range(1, len(self.segments) - 1):
            if self.segments[i].x == loc[0] and self.segments[i].y == loc[1]:
                return True
