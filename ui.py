#/usr/bin/python3

import pygame, time
from attributes import*
from pygame.locals import*
import city

class UI():
    def __init__(self):
        self.isMenuOpen = False
        self.isMenuOpening = False
        self.isMenuClosing = False
        self.coverage = 0
    
    class Button():
        def __init__(self, bTop, bLeft, bColor, bText, font):
            self.bTop = bTop
            self.bLeft = bLeft
            self.bColor = bColor
            self.bText = bText
            self.font = font
            self.clickable = True
            self.visible = True
            self.handler = None
        
        def onClick(self, handler):
            if self.clickable and self.visible:
                self.handler = handler
        
        def draw(self, surf):
           pygame.draw.rect(surf, self.bColor, (self.bTop, self.bLeft, BUTTONWIDTH, BUTTONHEIGHT)) 
           makeText(bText, bColor, bTop + BUTTONWIDTH / 2, bLeft, self.font)
        
    def createButton(self, surf, bTop, bLeft, bColor, bText):
        button = Button(bTop, bLeft, bColor, bText)
        button.draw(surf)
        return button

    def drawRect(self, surf):
        pygame.draw.rect(surf, ORANGE, (0, 0, WINDOWWIDTH, UIRECTSIZE / 5))
    
    def drawMoney(self, surf, money, font):
        (textSurf, textRect) = makeText("Money: " + str(money), WHITE, 0, 0, font)
        surf.blit(textSurf, textRect)
    
    def drawRTime(self, surf, rTime, font):
        rTimeSTR = "Remaining time: %.2f" % rTime if rTime > 0.0 else "Remaining time: 0.00"
        (textSurf, textRect) = makeText(rTimeSTR, WHITE, WINDOWWIDTH / 2, 0, font)
        surf.blit(textSurf, textRect)

    def printInventory(self, surf, iObj, font):
        if self.isMenuOpen:
            itemx = UIRECTSIZE / 20
            itemy = WINDOWHEIGHT / 5
            for i in range(NUMBEROFITEMS):
                (textSurf, textRect) = makeText(iObj.getInventoryEntry(i), WHITE, itemx, itemy, font)
                surf.blit(textSurf, textRect)
                itemy += MENUFONTSIZE + 1

            if type(iObj) == city.City:
                for i in range(NUMBEROFITEMS):
                    pass



    def drawMenuOpeningAnimation(self, surf):
        if(self.isMenuOpen == False or self.isMenuClosing):
            if(self.isMenuOpening == False):
                self.isMenuOpening = True
                self.isMenuClosing = False
                #self.coverage = 0
            
            if(self.isMenuOpening):
                self.coverage += MENUANIMATIONSPEED

            
            if(self.coverage >= 1):
                self.isMenuOpen = True
                self.isMenuOpening = False

        pygame.draw.rect(surf, ORANGE, (0, UIRECTSIZE / 5, UIMENUSIZE * self.coverage, WINDOWHEIGHT))

    def drawMenuClosingAnimation(self, surf):
        if(self.coverage >= 0):
            if(self.isMenuClosing == False):
                self.isMenuClosing = True
                self.isMenuOpening = False
                self.isMenuOpen = False
                #self.coverage = 1
            
            if(self.isMenuClosing):
                self.coverage -= MENUANIMATIONSPEED

            if(self.coverage <= 0):
                self.isMenuClosing = False
    
        pygame.draw.rect(surf, ORANGE, (0, UIRECTSIZE / 5, UIMENUSIZE * self.coverage, WINDOWHEIGHT))

    def drawCityMenu(self, surf, city, font):
        if self.isMenuOpen:
            (textSurf, textRect) = makeText(city.name, WHITE, WINDOWHEIGHT / 8, UIRECTSIZE / 5, font) 
            surf.blit(textSurf, textRect)
            self.printInventory(surf,city, font)
  
    def clearInv(self, surf):
        if self.isMenuOpen:
            self.drawRect(surf)
        
def makeText(text, color, top, left, font):
    # create the Surface and Rect object for some text
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)
    