import csv
import os

full_path = os.path.expanduser('D:\Diplom\DataSet\Data.csv')

_numberTemperatureForFile = -1
_numberPowerConsumptionForFile = 8


class CVSDataHelper:
    def __init__(self, full_path=os.path.expanduser('D:\Diplom\DataSet\Data.csv')):
        self.full_path = full_path

    @staticmethod
    def getOutsideTemperatureForDate(date):
        with open(full_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        temperature = spamreader[1][_numberTemperatureForFile]
        return temperature

    @staticmethod
    def getOutsideTemeratureForNumber(number):
        with open(full_path, newline='') as csvfile:
            data = list(csv.reader(csvfile, delimiter=';', quotechar='|'))
            temperature = data[number][_numberTemperatureForFile]
        return float(temperature)

    @staticmethod
    def getPowerConsumptionForNumber(number):
        with open(full_path, newline='') as csvfile:
            data = list(csv.reader(csvfile, delimiter=';', quotechar='|'))
            temperature = data[number][_numberPowerConsumptionForFile]
        return float(temperature)
