from dataclasses import dataclass
@dataclass
class paramSystem:
    #Заданая температура
    setTemperature = 20
    # Коэффициент теплоносителя
    coefficientCoolant = 20
    # Стартовые параметры
    startHeaterTemperature = 20.0
    # Длинна полинома Лагранжа для пид регулятора
    lengthLagrangePolinomial = 4
    # Количество комнат (Пока модель одномерная нужно будет потом сделать трехмерной)
    countRoom = 3
    # ручной ввод значений пид регулятора
    autoFindPidVarible = True
    #Количество дней модуляции
    day = 20
    # раз в сколько дней пересчитывать пид регулятор
    module_day = 2
    #На сколько частей бить день в расчетах
    tochnst = 5
    # сколько последних значений брать для интегральной части пид регулятора
    countPoint = 20
    # Коэффициент для Модели Здания 1 мерного 2a+b<1
    # a – коэффициент взаимосвязи двух комнат
    # TODO: преписать на массив 6 значний
    a = 0.01
    # γ-коэффициент передачи тепла от системы отопления в комнате в температуру помещения
    y = 0.04 / tochnst
    # Уменьшение дней, а именно в функици 2 для перрерачета линейного спуска
    days_calculate_fun2 = 5