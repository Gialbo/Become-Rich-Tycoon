#/usr/bin/python3

# Become Rich Tycoon
# Made by Gilberto Manunza
# A simple commerce based tycoon game

import pygame, sys
from city import *
from vehicle import *
from pygame.locals import *
from attributes import *


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event 
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Became Rich Tycoon')

    cities = []
    cities.append(City(400, 300))
    cities.append(City(250, 500))
    
    vehicle = Vehicle(cities[0])
    vehicle.setVehicleDestination(cities[1])
    vehicles = []
    vehicles.append(vehicle)

    selvehicle = None

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        for city in cities:
            city.drawCity(DISPLAYSURF)
        vehicle.drawVehicle(DISPLAYSURF)

        checkForQuit()

        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

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
            vehiclehig = None
        if vehiclehig == None and cityhig == None and mouseClicked:
            selvehicle = None

        if selvehicle != None:
            selvehicle.highlightVehicle(DISPLAYSURF)
        vehicle.travel()
        vehicle.isArrived()
        
        # Redraw the screen and wait a clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)

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
