#/usr/bin/python3

import pygame, random, csv
from inventory import *
from attributes import *
from pygame.locals import *

class City():
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.relx = self.x
        self.rely = self.y
        # vector pointing at the center of the city
        self.cityVec = pygame.math.Vector2(x + (CITYSIZE / 2), y + (CITYSIZE / 2))
        self.color = random.choice(CITYCOLORS)
        self.cityRect = pygame.Rect(x, y, CITYSIZE, CITYSIZE)
        self.inventory = Inventory()
        self.city_data = self.generateData()
        self.inventory.initializeInventory(self.city_data)
        self.setBuySellPrice()
    
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
        return "%s %d UNITS BUY: %.2f SELL: %.2f" % (entryItem.name, entryItem.quantity, entryItem.buyvalue, entryItem.sellvalue)
        # old version
        #return entryItem.name + " " + str(entryItem.quantity) + " BUY: " + str(entryItem.buyvalue) + " SELL: " +str(entryItem.sellvalue)

    def generateData(self):
        city_data = {}     
        file_name = self.name + "_data.csv"
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            isFirst = True
            for row in csv_reader:
                if not isFirst:
                    dict_line = {}
                    dict_line["q_mult"] = float(row[1])
                    dict_line["d_prod"] = float(row[2])
                    dict_line["d_cons"] = float(row[3])
                    dict_line["b_pmul"] = float(row[4])
                    city_data[row[0].strip()] = dict_line
                isFirst = False
        
        print(city_data)
        return city_data

    def setBuySellPrice(self):
        for name in self.city_data:
            good_data = self.city_data.get(name, None)
            good = self.inventory.get(name)
            diff = (good_data["d_cons"] / good_data["d_prod"]) * good_data["b_pmul"] / good.quantity * 1000
            good.buyvalue = good.basevalue - diff / 2
            good.sellvalue = good.basevalue + diff * 2


                    
                    


