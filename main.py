import random as rnd

import numpy as np
from matplotlib.pyplot import plot, show

from DataHelper.CVSDataHelper import CVSDataHelper
from MathObject.Room import Room
from PID.PID import PID

global x, result, index, build, temperature, control, integral, error

setTemperature = 20
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


def initialize():
    global x, result, index, build, temperature, control, error
    build = [Room(a, b, y, startHeaterTemperature, startOutsideTemperature)]
    result = [setTemperature]
    index = 0
    temperature = [startOutsideTemperature]
    control = [startHeaterTemperature]
    error = [0]
    CVSDataHelper()
    PID(0.9, 0.9, 0.2, setTemperature)
    for it in range(countRoom - 1):
        build.append(Room(a, b, y, startHeaterTemperature, startOutsideTemperature))


def observe():
    global index, result, arithmeticMeanTemperatureInBuild, error
    _sumTemperature = sum(c.temperatureSelf for c in build)
    _maxTemperature = max(build, key=lambda x: x.temperatureSelf).temperatureSelf
    _minTemperature = min(build, key=lambda x: x.temperatureSelf).temperatureSelf
    arithmeticMeanTemperatureInBuild = _sumTemperature / len(build)
    result.append(arithmeticMeanTemperatureInBuild)
    error.append(abs(arithmeticMeanTemperatureInBuild - setTemperature))
    index += 1


def update(t):
    global temperature, control, integral, result
    _outsideTemperature = CVSDataHelper.getOutsideTemeratureForNumber(t)
    _heaterTemperature = PID.getControlAction(result[(lengthLagrangePolinomial * -1):])
    control.append(_heaterTemperature)
    temperature.append(_outsideTemperature)
    for it in range(-1, countRoom - 1):
        build[it].setNewTemperature(build[it - 1].temperatureSelf, build[it + 1].temperatureSelf, _outsideTemperature,
                                    _heaterTemperature)


def main():
    initialize()
    for t in range(30):
        update(t)
        observe()
    print(max(error))
    plot(control)
    plot(result)
    plot(temperature)
    show()


if __name__ == '__main__':
    main()
