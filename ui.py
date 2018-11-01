#/usr/bin/python3

import pygame, time
from attributes import*
from pygame.locals import*

class UI():
    def __init__(self):
        self.isMenuOpen = False
        self.isMenuOpening = False
        self.isMenuClosing = False
        self.coverage = 0

    def drawRect(self, surf):
        pygame.draw.rect(surf, ORANGE, (0, 0, WINDOWWIDTH, UIRECTSIZE / 5))
    
    def drawMoney(self, surf, money, font):
        (textSurf, textRect) = self.makeText("Money: " + str(money), WHITE, 0, 0, font)
        surf.blit(textSurf, textRect)
    
    def drawRTime(self, surf, rTime, font):
        rTimeSTR = "Remaining time: %.2f" % rTime if rTime > 0.0 else "Remaining time: 0.00"
        (textSurf, textRect) = self.makeText(rTimeSTR, WHITE, WINDOWWIDTH / 2, 0, font)
        surf.blit(textSurf, textRect)

    def drawMenuOpeningAnimation(self, surf):
        if(self.isMenuOpen == False):
            if(self.isMenuOpening == False):
                self.isMenuOpening = True
                self.coverage = 0
            
            if(self.isMenuOpening):
                self.coverage += MENUANIMATIONSPEED

            
            if(self.coverage >= 1):
                self.isMenuOpen = True
                self.isMenuOpening = False

        pygame.draw.rect(surf, ORANGE, (0, UIRECTSIZE / 5, UIMENUSIZE * self.coverage, WINDOWHEIGHT))

    def drawMenuClosingAnimation(self, surf):
        if(self.isMenuOpen):
            if(self.isMenuClosing == False):
                self.isMenuClosing = True
                self.coverage = 1
            
            if(self.isMenuClosing):
                self.coverage -= MENUANIMATIONSPEED

            if(self.coverage <= 0):
                self.isMenuOpen = False
                self.isMenuClosing = False
    
        pygame.draw.rect(surf, ORANGE, (0, UIRECTSIZE / 5, UIMENUSIZE * self.coverage, WINDOWHEIGHT))


        
    def makeText(self, text, color, top, left, font):
        # create the Surface and Rect object for some text
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)  