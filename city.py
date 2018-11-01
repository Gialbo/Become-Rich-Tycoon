#/usr/bin/python3

import pygame, random
from inventory import *
from attributes import *
from pygame.locals import *

class City():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.relx = self.x
        self.rely = self.y
        # vector pointing at the center of the city
        self.cityVec = pygame.math.Vector2(x + (CITYSIZE / 2), y + (CITYSIZE / 2))
        self.color = random.choice(CITYCOLORS)
        self.cityRect = pygame.Rect(x, y, CITYSIZE, CITYSIZE)
        self.inventory = Inventory()
    
    def drawCity(self, surf):
        if(self.relx < WINDOWWIDTH and self.rely < WINDOWHEIGHT):
            pygame.draw.rect(surf, self.color, (self.relx, self.rely, CITYSIZE, CITYSIZE))
    
    def updateRelCoords(self, cameraX, cameraY):
        self.relx = self.x + cameraX
        self.rely = self.y + cameraY
        self.cityRect.x = self.relx
        self.cityRect.y = self.rely
    
    def highlightCity(self, surf):
        pygame.draw.rect(surf, HIGHLIGHTCOLOR, (self.relx - (HIGHLIGHTOFFSET / 2), self.rely - (HIGHLIGHTOFFSET / 2), CITYSIZE + HIGHLIGHTOFFSET, CITYSIZE + HIGHLIGHTOFFSET), 4)
    
    def getInventoryEntry(self, n):
        entryItem = self.inventory.inventory[n]
        return entryItem.name + " " + str(entryItem.quantity) + " " + str(entryItem.effectivevalue)

