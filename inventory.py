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
