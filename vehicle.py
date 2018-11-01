import pygame, random, math, time
from city import *
from attributes import *
from enum import Enum

VehicleState = Enum('State', 'ARRIVED TRAVELLING')

class Vehicle():
    def __init__(self, city):
        self.city = city
        self.x = city.x + CITYSIZE / 2
        self.y = city.y + CITYSIZE / 2
        self.relx = self.x
        self.rely = self.y
        self.destination = None
        self.state = VehicleState.ARRIVED
        self.color = random.choice(VEHICLECOLORS)
        self.vehicleRect = pygame.Rect(self.x - VEHICLERADIUS, self.y - VEHICLERADIUS, VEHICLERADIUS * 2, VEHICLERADIUS * 2)

    
    def drawVehicle(self, surf):
        if(self.relx < WINDOWWIDTH and self.rely < WINDOWHEIGHT):
            pygame.draw.circle(surf, self.color, (int(self.relx), int(self.rely)), VEHICLERADIUS)
        #Use for debugging
        #pygame.draw.rect(surf,self.color, self.vehicleRect)

    def updateRelCoords(self, cameraX, cameraY):
        self.relx = self.x + cameraX
        self.rely = self.y + cameraY
        self.vehicleRect.x = self.relx
        self.vehicleRect.y = self.rely

    def setVehicleDestination(self, destination):
        if(self.destination == None and destination != self.city):
            self.destination = destination
            self.vMov = self.destination.cityVec - self.city.cityVec
            self.rTime = (self.vMov.length() / VEHICLESPEED) * (FPS / 1000)
            self.vMov = self.vMov.normalize()
            self.elTime = 0
            self.startTime = time.time()
    
    def travel(self):
        if(self.destination != None):
            self.x += self.vMov.x * VEHICLESPEED
            self.y += self.vMov.y * VEHICLESPEED
            self.vehicleRect.left, self.vehicleRect.top = self.x - VEHICLERADIUS, self.y - VEHICLERADIUS
            self.state = VehicleState.TRAVELLING
            self.elTime = time.time() - self.startTime

    def isArrived(self):
        if self.destination != None and self.destination.cityRect.collidepoint(self.relx, self.rely):
            self.state = VehicleState.ARRIVED
            self.x, self.y = self.destination.cityVec
            self.vehicleRect.left, self.vehicleRect.top = self.x - VEHICLERADIUS / 2, self.y - VEHICLERADIUS / 2
            self.city = self.destination
            self.destination = None
            self.rTime = None
    
    def highlightVehicle(self, surf):
        pygame.draw.circle(surf, HIGHLIGHTCOLOR, (int(self.relx), int(self.rely)), VEHICLERADIUS + 1, 4)

    