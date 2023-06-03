import numpy

from numpy import array
from scipy.optimize import curve_fit
import sqlite3 as sl
import telebot

from Selenide.tempPars import get_next_temperature
from math_calculate_main import main

con = sl.connect('DB/thecode.db')
bot = telebot.TeleBot("Token")


@bot.message_handler(commands=['help'])
# TODO: тут нужно написать -h
def send_welcome(message):
    bot.reply_to(message, "Есть несколько команд: /object, /temp город, /target")


def get_list_house():
    # TODO: пока будет заглушка дальше подключение к бд
    return "TestHous"


@bot.message_handler(commands=['object'])
def send_welcome(message):
    answer = get_list_house()
    bot.send_message(message.from_user.id, "" + answer)

@bot.message_handler(commands=['target'])
def send_welcome(message):
    answer = main()
    bot.send_message(message.from_user.id, "" + answer)

def get_temperature_outside(message):
    return get_next_temperature(message)


@bot.message_handler(commands=['temp'])
def send_temperature(message):
    try:
        var = message.text.split(' ')[1]
        try:
            answer = get_temperature_outside(var)
            bot.send_message(message.from_user.id, "" + answer)
        except:
            bot.send_message(message.from_user.id, "Не получилось получить температуру в городе " + var)
    except:
        bot.send_message(message.from_user.id, "Не введен или не распознан город, пример /temp Москва")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "":
        bot.send_message(message.from_user.id, "Чем я могу тебе помочь?")
    else:
        bot.send_message(message.from_user.id, "Работа с ботом происходит с помощью команд. Напиши /help.")


bot.infinity_polling()


# TODO: не совсем правильно считает температуру здания в ней всегда остается положительная температура, нужно вводить параметр б и по новой все дебажить


# TODO: Переписать на глобальную переменную или еще как-то передать в количество дней для анализа


# TODO: функция рассчета для 2 дней


# формат x как вектор комнат те x[0] в первой комнате x[1] во второй и тд + последний x вседа температура нагревателя]
def funcTempRoom(x, A0, Y1, A2):
    return (x[1] - x[0]) * A0 + (x[2] - x[0]) * A2 + Y1 * x[3]
    # A0x0+A2x2 - A0x[0]-A2x[0] + Y1*x[1]
    # (A0+A2)*(-1*x[0])+Y1*x[1] + k
    # k = A0*x1 +A2*x2  = Ax1-A2x1 + A2x2  = Ax1 + A2(x2-x1)
    # A = A0+A2 | A0 =A -A2
    # return -1*A*x[0]+Y1*x[1]+A*x1 + A2*(x2-x1)
    # TODO: F(x) = a * x ^ 3
    #   F(x[0],x[1]) = (a-x[0])*b + c*x[1] + d*x[0]


def funcT(x, a, b, c, d):
    return (a - x[0]) * b + c * x[1] + d * x[0]


# TODO: 2 графика 1) Реальное x- калории y - температура f1 - то что было f2 - реком
# на малине сервер в телеграм бот


def delete(x, a, b, c, d):
    # TODO: создать матрицу со значениями initialize_build_struct()
    x0 = array([12, 11, 13, 15, 16, 16, 15, 14, 15, 12, 11, 12, 8, 10, 9, 7, 6])
    x1 = array([12, 11, 13, 15, 16, 16, 15, 14, 15, 12, 11, 12, 8, 10, 9, 7, 6])
    x2 = array([12, 11, 13, 15, 16, 16, 15, 14, 15, 12, 11, 12, 8, 10, 9, 7, 6])
    TempHeater = numpy.random.normal(loc=10, scale=0.2, size=len(x0))
    z = numpy.random.normal(loc=10, scale=0.2, size=len(x0))
    # TODO: Для крайнего элемета матрицы построить посчитать коэффицент A Y
    # TODO: расчитать примерные коэффиценты для других
    # TODO: Для крайнего элемета матрицы построить посчитать коэффицент A Y
    # TODO: расчитать примерные коэффиценты для других
    # TODO: Усреднить значния коэффициентов
    print("step")
    p0 = [1.0, 1.0, 1.0]
    params, _ = curve_fit(funcTempRoom, (x0, x1, x2, TempHeater), z, p0)

    print("params: ", params)
