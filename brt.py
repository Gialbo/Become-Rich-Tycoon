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

    mousex = 0 # used to store x coordinate of mouse event 
    mousey = 0 # used to store y coordinate of mouse event
    camerax = 0 
    cameray = 0 
    pygame.display.set_caption('Became Rich Tycoon')

    cities = []
    cities.append(City(400, 300))
    cities.append(City(250, 500))
    
    vehicle = Vehicle(cities[0])
    vehicle.setVehicleDestination(cities[1])
    vehicles = []
    vehicles.append(vehicle)
    vehicle = Vehicle(cities[1])
    vehicle.setVehicleDestination(cities[0])
    vehicles.append(vehicle)

    ui = UI()

    money = 2000
    selvehicle = None

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        for city in cities:
            city.updateRelCoords(camerax, cameray)
            city.drawCity(DISPLAYSURF)
        for vehicle in vehicles:
            vehicle.updateRelCoords(camerax, cameray)
            vehicle.drawVehicle(DISPLAYSURF)
        ui.drawRect(DISPLAYSURF)
        ui.drawMoney(DISPLAYSURF, money, BASICFONT)
        if(selvehicle and selvehicle.rTime):
            ui.drawRTime(DISPLAYSURF, selvehicle.rTime - selvehicle.elTime, BASICFONT)

        checkForQuit()


        for event in pygame.event.get(): # event handling loop
            mousex, mousey, mouseClicked = getMouseEvents(event, mousex, mousey, mouseClicked)
            camerax, cameray = getCameraMovement(event, camerax, cameray)

        cityhig = getCityAtPixel(cities, mousex, mousey)
        vehiclehig = getVehicleAtPixel(vehicles, mousex, mousey)

        if cityhig != None:
            cityhig.highlightCity(DISPLAYSURF)
        if cityhig != None and mouseClicked:
            cityhig.highlightCity(DISPLAYSURF)
            if selvehicle != None:
                selvehicle.setVehicleDestination(cityhig)

        if vehiclehig != None:
            vehiclehig.highlightVehicle(DISPLAYSURF)
        if vehiclehig != None and mouseClicked:
            vehiclehig.highlightVehicle(DISPLAYSURF)
            selvehicle = vehiclehig
        if vehiclehig == None and cityhig == None and mouseClicked:
            selvehicle = None

        if selvehicle != None:
            selvehicle.highlightVehicle(DISPLAYSURF)
            ui.drawMenuOpeningAnimation(DISPLAYSURF)
        else:
            ui.drawMenuClosingAnimation(DISPLAYSURF)

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

