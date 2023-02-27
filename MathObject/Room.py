import random

class Room():
    def __init__(self, a, y):
        _Q = random.randrange(190, 210) / 10.0
        self.temperatureSelf =_Q
        # TODO: преписать на массив 6 значний
        self.a = a
        self.y = y

    def setNewTemperature(self, sosedy, outsideTemerature: float, heaterTemperature):
        if sosedy.left is None:
            leftTemp = outsideTemerature
        else:
            leftTemp = sosedy.left.temperatureSelf
        if sosedy.right is None:
            righTemp = outsideTemerature
        else:
            righTemp = sosedy.right.temperatureSelf
        if sosedy.top is None:
            topTemp = outsideTemerature
        else:
            topTemp = sosedy.top.temperatureSelf
        if sosedy.bot is None:
            botTemp = outsideTemerature
        else:
            botTemp = sosedy.bot.temperatureSelf
        if sosedy.up is None:
            upTemp = outsideTemerature
        else:
            upTemp = sosedy.up.temperatureSelf
        if sosedy.down is None:
            downTemp = outsideTemerature
        else:
            downTemp = sosedy.down.temperatureSelf
        # TODO: преписать на массив 6 значний
        incomeRooms = self.a * (leftTemp - self.temperatureSelf) + self.a*(righTemp - self.temperatureSelf) + self.a*(topTemp - self.temperatureSelf) + self.a*(botTemp - self.temperatureSelf) + self.a*(upTemp - self.temperatureSelf) + self.a*(downTemp - self.temperatureSelf)
        incomeHeater = self.y * heaterTemperature
        self.temperatureSelf = self.temperatureSelf + incomeRooms + incomeHeater


    def returnTempetatuteSelf(self):
        return self.temperatureSelf