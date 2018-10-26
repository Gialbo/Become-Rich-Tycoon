#/usr/bin/python3

import pygame, random
from attributes import *
from pygame.locals import *

class City():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # vector pointing at the center of the city
        self.cityVec = pygame.math.Vector2(x + (CITYSIZE / 2), y + (CITYSIZE / 2))
        self.color = random.choice(CITYCOLORS)
        self.cityRect = pygame.Rect(x, y, CITYSIZE, CITYSIZE)
    
    def drawCity(self, surf):
        pygame.draw.rect(surf, self.color, (self.x, self.y, CITYSIZE, CITYSIZE))
    
    def highlightCity(self, surf):
        pygame.draw.rect(surf, HIGHLIGHTCOLOR, (self.x - (HIGHLIGHTOFFSET / 2), self.y - (HIGHLIGHTOFFSET / 2), CITYSIZE + HIGHLIGHTOFFSET, CITYSIZE + HIGHLIGHTOFFSET), 4)

