import random


class Room():
    global temperatureSelf, a, b, y, heaterTemperature, outsideTemperature

    def __init__(self, a, b, y,
                 heaterTemperature, outsideTemperature):
        _v = random.randrange(-1350, 375) / 1000.0
        _w = random.randrange(57, 70) / 10.0
        _Q = random.randrange(190, 210) / 10.0
        self.temperatureSelf =  _Q
        self.a = a
        self.b = b
        self.y = y
        self.heaterTemperature = heaterTemperature
        self.outsideTemperature = outsideTemperature

    def setNewTemperature(self, temperatureLeft, temperatureRight, outsideTemerature: float, heaterTemperature):
        global temperatureSelf, a, b, y
        _v = random.randrange(0, 375) / 1000.0
        _w = random.randrange(57, 70) / 10.0
        self.temperatureSelf = (1 - 2 * self.a - self.b) * self.temperatureSelf + self.a * (
                    temperatureLeft + temperatureRight) + self.b * outsideTemerature + self.y * heaterTemperature * _v + _w
