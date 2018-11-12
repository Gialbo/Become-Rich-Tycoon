from inventory import *
from item import *
from attributes import *

class Inventory():
    def __init__(self):
        self.inventory = []
        fp = open("item_list.txt", "r")
        for i in range(NUMBEROFITEMS):
            line = fp.readline()
            values = line.split(" ")
            item = Item(values[0], 0, int(values[1]))
            self.inventory.append(item)
    
    def initializeInventory(self, city_data):
        for i in range(0, len(self.inventory)):
            name = self.inventory[i].name
            good_data = city_data.get(name, None)
            self.inventory[i].quantity = good_data["q_mult"] * DEFAULTQUANTITY
            self.inventory[i].basevalue = good_data["b_pmul"] * self.inventory[i].basevalue

    def updateBuySellPrice(self, good_name, buy_price, sell_price):
        ind = self.inventory.index(good_name)
        self.inventory[ind].buyvalue = buy_price
        self.inventory[ind].sellvalue = sell_price
    
    def get(self, good):
        for i in range(NUMBEROFITEMS):
            if self.inventory[i].name  == good:
                break
        return self.inventory[i]
