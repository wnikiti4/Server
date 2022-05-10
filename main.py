import random as rnd
from dataclasses import dataclass
import numpy as np
from matplotlib.pyplot import plot, show
from MQTT.PushMQTT import push_mail, get_temperature_in_valve
from Selenide.ParseTemperature import  get_one_temperature
from DataHelper.CVSDataHelper import CVSDataHelper
from MathObject.Room import Room
from PID.PID import PID

global x, result, index, build, temperature, control, integral, error, consumption

setTemperature = 25
# Коэффициент теплоносителя
coefficientCoolant = 20
# Коэффициент для Модели Здания 1 мерного
a = 0.1
b = 0.5
y = 0.8
# Коэффициенты для Модели Здания 2 комнаты
A = np.array([[0.1, 1 - 2 * a - b], [1 - 2 * a - b, 0.1]])
Vk = np.array([rnd.randrange(-1350, 372) / 1000.0, rnd.randrange(-1350, 372) / 1000.0])

# Стартовые параметры
arithmeticMeanTemperatureInBuild = setTemperature
startHeaterTemperature = 20.0
startOutsideTemperature = 5.0
# Длинна полинома Лагранжа для пид регулятора
lengthLagrangePolinomial = 4
# Количество комнат
countRoom = 30


@dataclass
class PidValue:
    k1: float = 2.0
    k2: float = 0.9
    k3: float = 0.2


bestPIDValue: PidValue


def initialize(temperature_in_valve, startOutsideTemperature):
    global x, result, index, build, temperature, control, error, consumption
    build = [Room(a, b, y, temperature_in_valve, startOutsideTemperature)]
    result = [setTemperature]
    index = 0
    temperature = [startOutsideTemperature]
    control = [temperature_in_valve]
    error = [0]
    consumption = 0
    CVSDataHelper()
    PID(PidValue.k1, PidValue.k2, PidValue.k3, setTemperature)
    for it in range(countRoom - 1):
        build.append(Room(a, b, y, startHeaterTemperature, startOutsideTemperature))


def observe():
    global index, result, arithmeticMeanTemperatureInBuild, error, consumption
    _sumTemperature = sum(c.temperatureSelf for c in build)
    _maxTemperature = max(build, key=lambda x: x.temperatureSelf).temperatureSelf
    _minTemperature = min(build, key=lambda x: x.temperatureSelf).temperatureSelf
    arithmeticMeanTemperatureInBuild = _sumTemperature / len(build)
    result.append(arithmeticMeanTemperatureInBuild)
    error.append(abs(arithmeticMeanTemperatureInBuild - setTemperature))
    index += 1


def update(t):
    global temperature, control, integral, result, consumption
    _outsideTemperature = CVSDataHelper.getOutsideTemeratureForNumber(t)
    _heaterTemperature = PID.getControlAction(result[(lengthLagrangePolinomial * -1):])
    consumption += abs(_heaterTemperature)
    control.append(_heaterTemperature)
    temperature.append(_outsideTemperature)
    for it in range(-1, countRoom - 1):
        build[it].setNewTemperature(build[it - 1].temperatureSelf, build[it + 1].temperatureSelf, _outsideTemperature,
                                    _heaterTemperature)


def main():
    global answer, bestPIDValue
    # temperature_in_valve = get_temperature_in_valve
    # _outsideTemperature = get_one_temperature("2022-05-09 ", "22:00")
    temperature_in_valve = 50
    _outsideTemperature = 0
    local_error = 10000000
    local_consumption = 10000000
    print("Пользовательские настройки? y/n")
    first_answer = input()
    if first_answer == "y":
        answer = "y"
        while answer == "y":
            print("Введите k1:")
            PidValue.k1 = input()
            print("Введите k2:")
            PidValue.k2 = input()
            print("Введите k3:")
            PidValue.k3 = input()
            initialize(temperature_in_valve, _outsideTemperature)
            for t in range(30):
                update(t)
                observe()
            print(max(error))
            print(consumption)
            plot(control)
            plot(result)
            plot(temperature)
            show()
            bestPIDValue = PidValue
            print("Продолжить настройку? y/n")
            answer = input()
    if first_answer == "n":
        print("происходит расчет...")
        for k1 in range(-100, 100):
            if (k1 % 10 == 0): print(".")
            for k2 in range(-100, 100):
                for k3 in range(-100, 100):
                    PidValue.k1 = k1
                    PidValue.k2 = k2
                    PidValue.k3 = k3
                    initialize(temperature_in_valve, _outsideTemperature)
                    for t in range(30):
                        update(t)
                        observe()
                    if (local_error > max(error)) and (local_consumption > consumption):
                        local_error = max(error)
                        local_consumption = consumption
                        bestPIDValue = PidValue
        print(local_error)
        print(local_consumption)
        print(str(bestPIDValue))
        plot(control)
        plot(result)
        plot(temperature)
        show()
    push_mail(str(bestPIDValue))


if __name__ == '__main__':
    main()
