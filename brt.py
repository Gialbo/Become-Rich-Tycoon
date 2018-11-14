#/usr/bin/python3

# Become Rich Tycoon
# Made by Gilberto Manunza
# A simple commerce based tycoon game

import pygame, sys, time
from city import *
from vehicle import *
from pygame.locals import *
from attributes import *
from ui import *

pygame.init()
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
MENUFONT = pygame.font.Font('freesansbold.ttf', MENUFONTSIZE)

money = 2000
ui = UI()

def main():
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


    mousex = 0 # used to store x coordinate of mouse event 
    mousey = 0 # used to store y coordinate of mouse event
    camerax = 0 
    cameray = 0 
    pygame.display.set_caption('Became Rich Tycoon')

    cities = []
    cities.append(City("Milano", 400, 300))
    cities.append(City("Torino", 250, 500))
    
    vehicle = Vehicle("TurboDaily", cities[0])
    vehicle.setVehicleDestination(cities[1])
    vehicles = []
    vehicles.append(vehicle)
    vehicle = Vehicle("IvecoCargo", cities[1])
    vehicle.setVehicleDestination(cities[0])
    vehicles.append(vehicle)


    selvehicle = None
    selcity = None
    buttonhig = None
    (button_sell, button_buy) = (None, None)

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        for city in cities:
            # update relative camera coordinates
            city.updateRelCoords(camerax, cameray)
            # draw city
            city.drawCity(DISPLAYSURF)
        for vehicle in vehicles:
            # update relative camera coordinates
            vehicle.updateRelCoords(camerax, cameray)
            # draw vehicle
            vehicle.drawVehicle(DISPLAYSURF)
        # draw UI upper bar
        ui.drawRect(DISPLAYSURF)
        # display money on screen
        ui.drawMoney(DISPLAYSURF, money, BASICFONT)
        # display remaining time until destination if there's a vehicle moving
        if selvehicle and selvehicle.rTime:
            ui.drawRTime(DISPLAYSURF, selvehicle.rTime - selvehicle.elTime, BASICFONT)

        checkForQuit()

        for event in pygame.event.get(): # event handling loop
            mousex, mousey, mouseClicked = getMouseEvents(event, mousex, mousey, mouseClicked)
            camerax, cameray = getCameraMovement(event, camerax, cameray)

        # get object at mouse position
        cityhig = getCityAtPixel(cities, mousex, mousey)
        vehiclehig = getVehicleAtPixel(vehicles, mousex, mousey)
        buttonhig = getButtonAtPixel(button_buy, button_sell, mousex, mousey)
        # handling city selection
        if cityhig != None:
            cityhig.highlightCity(DISPLAYSURF)
        if cityhig != None and mouseClicked:
            selcity = cityhig
            cityhig.highlightCity(DISPLAYSURF)
            # assign a destination to selected vehicle
            if selvehicle != None:
                selvehicle.setVehicleDestination(cityhig)

        # handling vehicle selection
        if vehiclehig != None:
            vehiclehig.highlightVehicle(DISPLAYSURF)
        if vehiclehig != None and mouseClicked:
            vehiclehig.highlightVehicle(DISPLAYSURF)
            selvehicle = vehiclehig
        if vehiclehig == None and cityhig == None and mouseClicked:
            if (not ui.isMenuOpen) or (not ui.uiRect.collidepoint(mousex, mousey)):
                selvehicle = None
                selcity = None

        # handle menu opening/closing animation
        if selvehicle != None or selcity != None:
            ui.drawMenuOpeningAnimation(DISPLAYSURF)
        else:
            ui.drawMenuClosingAnimation(DISPLAYSURF)

        if selvehicle != None:
            selvehicle.highlightVehicle(DISPLAYSURF)
            if selcity == None:
                ui.printInventory(DISPLAYSURF, selvehicle, MENUFONT)

        if selcity != None:
            selcity.highlightCity(DISPLAYSURF)
            ui.drawCityMenu(DISPLAYSURF, selcity, MENUFONT)
            (button_sell, button_buy) = ui.makeCityButtons(DISPLAYSURF, MENUFONT)
            assignHandlerToButtons(button_sell, button_buy, selcity, selvehicle)
        else:
            (button_sell, button_buy) = (None, None)

        # Handle buy/sell buttons
        if(buttonhig != None):
            buttonhig.highlight(DISPLAYSURF)
            if(mouseClicked and selvehicle != None and selcity != None):
                if(selvehicle.city == selcity):
                    buttonhig.eventClicked()
            

        for vehicle in vehicles:
            vehicle.travel()
            vehicle.isArrived()
        
        # Redraw the screen and wait a clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getCameraMovement(event, camerax, cameray):
    if(event.type == KEYUP):
        if event.key == K_UP:
            cameray += CAMERASPEED
        if event.key == K_DOWN:
            cameray -= CAMERASPEED
        if event.key == K_LEFT:
            camerax += CAMERASPEED
        if event.key == K_RIGHT:
            camerax -= CAMERASPEED

    return camerax, cameray

def getMouseEvents(event, mousex, mousey, mouseClicked):
    if event.type == MOUSEMOTION:
        mousex, mousey = event.pos
    if event.type == MOUSEBUTTONUP:
        mousex, mousey = event.pos
        mouseClicked = True
    return mousex, mousey, mouseClicked

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if  event.type ==  K_ESCAPE:
            terminate()
        pygame.event.post(event)

def terminate():
    pygame.quit()
    sys.exit()

def getCityAtPixel(cities, x, y):
    for city in cities:
        if city.cityRect.collidepoint(x,y):
            return city
    return None

def getVehicleAtPixel(vehicles, x, y):
    for vehicle in vehicles:
        if vehicle.vehicleRect.collidepoint(x,y):
            return vehicle
    return None

def getButtonAtPixel(buttonbuy, buttonsell, x, y):
    if(buttonbuy != None and buttonsell != None):
        for b in buttonbuy:
            if b.bRect.collidepoint(x,y):
                return b
        for b in buttonsell:
            if b.bRect.collidepoint(x,y):
                return b
    return None

def buy(quantity, goodToSell, goodToBuy):
    global money
    price = (goodToSell.buyvalue * quantity)
    if(money - price < 0):
        ui.showNoMoney(DISPLAYSURF, BASICFONT)
    else:
        money -= price
        goodToSell.quantity -= quantity
        goodToBuy.quantity += quantity
        goodToBuy.buyvalue += (price - goodToBuy.buyvalue) / quantity
        goodToBuy.sellvalue = goodToBuy.buyvalue

def sell(quantity, goodToSell, goodToBuy):
    global money
    if(goodToSell.quantity >= quantity):
        price = (goodToBuy.sellvalue * quantity)
        money += price
        goodToSell.quantity -= quantity
        goodToBuy.quantity += quantity

def assignHandlerToButtons(buttons_sell, buttons_buy, selcity, selvehicle):
    if(selcity != None and selvehicle != None and buttons_buy != None and buttons_sell != None):
        for n in range(NUMBEROFITEMS):
            quantity = 1
            tosell = selcity.inventory.inventory[n]
            tobuy = selvehicle.inventory.inventory[n]
            buttons_buy[n].onClick(buy, quantity, tosell, tobuy)
            tosell = selvehicle.inventory.inventory[n]
            tobuy = selcity.inventory.inventory[n]
            buttons_sell[n].onClick(sell, quantity, tosell, tobuy)

        

if __name__ == '__main__':
    main()

