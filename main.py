from dataclasses import dataclass
from random import random

import scipy.interpolate
import scipy.optimize

from matplotlib.pyplot import plot, show, legend
from scipy.optimize import minimize

from DataHelper.CVSDataHelper import CVSDataHelper
from MathObject.Room import Room
from PID.PID import PID
from DataSet.ParamSystem import paramSystem


@dataclass
class sosedy_val_A:
    up: float
    down: float
    left: float
    right: float
    top: float
    bot: float


@dataclass
class sosedy:
    up: Room
    down: Room
    left: Room
    right: Room
    top: Room
    bot: Room


def initialize_build_struct():
    #TODO: преписать на массив 6 значний
    build = [[[Room(paramSystem.a, paramSystem.y)] * paramSystem.countRoom] * paramSystem.countRoom] * paramSystem.countRoom
    for it in range(paramSystem.countRoom):
        for it2 in range(paramSystem.countRoom):
            for it3 in range(paramSystem.countRoom):
                # TODO: преписать на массив 6 значний
                build[it][it2][it3] = Room(paramSystem.a, paramSystem.y)
    return build


def find_arithmetic_mean_temp(build):
    sum_temp = 0
    for it in range(paramSystem.countRoom):
        for it2 in range(paramSystem.countRoom):
            for it3 in range(paramSystem.countRoom):
                sum_temp += build[it][it2][it3].returnTempetatuteSelf()
    return sum_temp / (paramSystem.countRoom**3)


def find_max_temp(build):
    point = None
    max_temp = build[0][0][0].returnTempetatuteSelf()
    for it in range(paramSystem.countRoom):
        for it2 in range(paramSystem.countRoom):
            for it3 in range(paramSystem.countRoom):
                if build[it][it2][it3].returnTempetatuteSelf() > max_temp:
                    max_temp = build[it][it2][it3].returnTempetatuteSelf()
                    point = it, it2, it3
    return max_temp , point



def find_min_temp(build):
    point = None
    min_temp = build[0][0][0].returnTempetatuteSelf()
    for it in range(paramSystem.countRoom):
        for it2 in range(paramSystem.countRoom):
            for it3 in range(paramSystem.countRoom):
                if build[it][it2][it3].returnTempetatuteSelf() < min_temp:
                    min_temp = build[it][it2][it3].returnTempetatuteSelf()
                    point = it, it2, it3
    return min_temp, point


def initialize_ambient_temp():
    dh = CVSDataHelper()
    _y = list()
    _x = list()
    for it in range(dh.getCountElement()):
        _y.append(dh.getOutsideTemeratureForNumber(it))
        _x.append(it)
    return scipy.interpolate.interp1d(_x, _y, kind='cubic')


def calculation_house_function(y_interp=None, build=None, startDay=0, endDay=paramSystem.day):
    result = [20]
    control = list()
    ambientTemp = list()
    _heaterTemperature = paramSystem.startHeaterTemperature
    error = list()
    for t in range(startDay * paramSystem.tochnst, endDay * paramSystem.tochnst):
        _outsideTemperature: float = y_interp(t)
        buildTemp = calculation_build_temp(_outsideTemperature, _heaterTemperature, build)
        _heaterTemperature = PID.getControlAction(result)
        # логическое ограничение системы, что можно подать температуру меньше чем температура в доме
        if _heaterTemperature < buildTemp:
            _heaterTemperature = buildTemp
        control.append(_heaterTemperature)
        ambientTemp.append(_outsideTemperature)
        result.append(buildTemp)
        error.append(abs(buildTemp - paramSystem.setTemperature))
    return error, control, result, ambientTemp


#TODO: не совсем правильно считает температуру здания в ней всегда остается положительная температура, нужно вводить параметр б и по новой все дебажить
def calculation_build_temp(_outsideTemperature, _heaterTemperature, build):
    for it in range(0, paramSystem.countRoom - 1, 1):
        for it2 in range(0, paramSystem.countRoom - 1, 1):
            for it3 in range(0, paramSystem.countRoom - 1, 1):
                if it == paramSystem.countRoom:
                    sosedy.right = None
                else:
                    sosedy.right = build[it+1][it2][it3]
                if it == 0:
                    sosedy.left = None
                else:
                    sosedy.left = build[it - 1][it2][it3]
                if it2 == paramSystem.countRoom:
                    sosedy.up = None
                else:
                    sosedy.up = build[it][it2+1][it3]
                if it2 == 0:
                    sosedy.down = None
                else:
                    sosedy.down = build[it][it2-1][it3]
                if it3 == paramSystem.countRoom:
                    sosedy.top = None
                else:
                    sosedy.top = build[it][it2][it3+1]
                if it3 == 0:
                    sosedy.bot = None
                else:
                    sosedy.bot = build[it][it2][it3-1]

                build[it][it2][it3].setNewTemperature(sosedy,_outsideTemperature,_heaterTemperature)
    min_temp = find_min_temp(build)
    av = find_arithmetic_mean_temp(build)
    max_temp = find_max_temp(build)
    return av

def main():
    # переписать на перерасчет каждые 2 дня
    # Разделить датасет на проверочную и для находжения коэффицентов
    # Сделать 2 результата: 1) в том когда 1 раз посчитали и дальше просто используем параметры 2) Пресчет каждые 3-4 меняем параметры пид регулятора
    param = [random(), random(), random()]
    param = find_pid_value(param, paramSystem.day)
    PID(param, 20)
    struct_build = initialize_build_struct()
    function_ambient_temp = initialize_ambient_temp()
    error_1, control_1, result_1, ambient_temp_1 = calculation_house_function(function_ambient_temp, struct_build)
    print(max(error_1))
    plot(control_1, label='Температура Нагревателя')
    plot(result_1, label='Температура Дома')
    plot(ambient_temp_1, label='Температура на Улице')
    #TODO: сделать перерасчет коэфПид регулятора каждые 3 дня и можно уже в статью кидать
    param = [random(), random(), random()]
    param = find_pid_value(param, 2)
    PID(param, 20)
    struct_build = initialize_build_struct()
    function_ambient_temp = initialize_ambient_temp()
    error_2, control_2, result_2, ambient_temp_2 = calculation_house_function(function_ambient_temp, struct_build)
    print(max(error_2))
    plot(control_2, label='Температура Нагревателя 2')
    plot(result_2, label='Температура Дома 2')
    legend()
    show()



def fun(param):
    PID(param, 20)
    struct_build = initialize_build_struct()
    function_ambient_temp = initialize_ambient_temp()
    error, control, result, ambient_temp = calculation_house_function(function_ambient_temp, struct_build)
    return max(error)

#TODO: функция рассчета для 2 дней
def fun2(param):
    PID(param, 20)
    struct_build = initialize_build_struct()
    function_ambient_temp = initialize_ambient_temp()
    error, control, result, ambient_temp = calculation_house_function(function_ambient_temp, struct_build, 0 , paramSystem.days_calculate_fun2)
    return max(error)


def find_pid_value(param, day):
    if day == paramSystem.day:
        return minimize(fun, param, method='Powell').x
    else:
        return minimize(fun2, param, method='Powell').x

if __name__ == '__main__':
    main()

