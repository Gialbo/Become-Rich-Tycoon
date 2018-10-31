#/usr/bin/python3

import pygame
from attributes import*
from pygame.locals import*

class UI():
    def drawRect(self, surf):
        pygame.draw.rect(surf, ORANGE, (0, 0, WINDOWWIDTH, UIRECTSIZE / 5))
    
    def drawMoney(self, surf, money, font):
        (textSurf, textRect) = self.makeText("Money: " + str(money), WHITE, 0, 0, font)
        surf.blit(textSurf, textRect)
    
    def drawRTime(self, surf, rTime, font):
        rTimeSTR = "Remaining time: %.2f" % rTime if rTime > 0.0 else "Remaining time: 0.00"
        (textSurf, textRect) = self.makeText(rTimeSTR, WHITE, WINDOWWIDTH / 2, 0, font)
        surf.blit(textSurf, textRect)
        
    def makeText(self, text, color, top, left, font):
        # create the Surface and Rect object for some text
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)  