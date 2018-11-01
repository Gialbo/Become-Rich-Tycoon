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


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    MENUFONT = pygame.font.Font('freesansbold.ttf', MENUFONTSIZE)


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

    ui = UI()

    money = 2000
    selvehicle = None
    selcity = None

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
            selvehicle = None
            selcity = None

        # handle menu opening/closing animation
        if selvehicle != None or selcity != None:
            ui.drawMenuOpeningAnimation(DISPLAYSURF)
        else:
            ui.drawMenuClosingAnimation(DISPLAYSURF)

        if selvehicle != None:
            selvehicle.highlightVehicle(DISPLAYSURF)
            ui.printInventory(DISPLAYSURF, selvehicle, MENUFONT)

        if selcity != None:
            selcity.highlightCity(DISPLAYSURF)
            ui.drawCityMenu(DISPLAYSURF, selcity, MENUFONT)
        
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
        

if __name__ == '__main__':
    main()

