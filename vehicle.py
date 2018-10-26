import pygame, random, math
from city import *
from attributes import *
from enum import Enum

VehicleState = Enum('State', 'ARRIVED TRAVELLING')

class Vehicle():
    def __init__(self, city):
        self.city = city
        self.x = city.x + CITYSIZE / 2
        self.y = city.y + CITYSIZE / 2
        self.destination = None
        self.state = VehicleState.ARRIVED
        self.color = random.choice(VEHICLECOLORS)
        self.vehicleRect = pygame.Rect(self.x, self.y, VEHICLERADIUS * 2, VEHICLERADIUS * 2)

    
    def drawVehicle(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), VEHICLERADIUS)

    def setVehicleDestination(self, destination):
        if(self.destination == None and destination != self.city):
            self.destination = destination
            self.vMov = self.destination.cityVec - self.city.cityVec
            self.vMov = self.vMov.normalize()
    
    def travel(self):
        if(self.destination != None):
            self.x += self.vMov.x * VEHICLESPEED
            self.y += self.vMov.y * VEHICLESPEED
            self.vehicleRect.left, self.vehicleRect.top = self.x, self.y
            self.state = VehicleState.TRAVELLING

    def isArrived(self):
        if self.destination != None and self.destination.cityRect.collidepoint(self.x, self.y):
            self.state = VehicleState.ARRIVED
            self.x, self.y = self.destination.cityVec
            self.vehicleRect.left, self.vehicleRect.top = self.x, self.y
            self.city = self.destination
            self.destination = None
    
    def highlightVehicle(self, surf):
        pygame.draw.circle(surf, HIGHLIGHTCOLOR, (int(self.x), int(self.y)), VEHICLERADIUS + 1, 4)

    