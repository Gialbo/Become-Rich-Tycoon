
class Item():
    def __init__(self, name, quantity, basevalue):
        self.name = name
        self.quantity = quantity
        self.basevalue = basevalue
        self.effectivevalue = self.basevalue
