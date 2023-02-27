from PID.Lagrange import LagrangePoly
from DataSet.ParamSystem import paramSystem

class PID:
    global _Ki, _Kp, _Kd

    def __init__(self, param, setpoint):
        global _setPoint, _Ki, _Kp, _Kd, _timeDiscrete
        _setPoint = setpoint
        _timeDiscrete = 1/paramSystem.tochnst
        _Kd = param[0]
        _Ki = param[1]
        _Kp = param[2]

    @staticmethod
    def getControlAction(value):
        global _Ki, _Kp, _Kd, _timeDiscrete
        # Пропорциональная
        proportional = (_setPoint - value[-1])
        # Интегральная часть, по методу трапеции
        integral = 0
        if paramSystem.countPoint > len(value):
            count_point = len(value)
        else:
            count_point = paramSystem.countPoint
        for it in range(1, count_point):
            trapezoidArea = 1 / 2 * (_setPoint - value[it] + _setPoint - value[it - 1]) * _timeDiscrete
            integral += trapezoidArea
        # TODO: Пропорциональная и интегральная +- работает а вот уже пропорциональная там пиздец и садамия нужно исправитьб
        # Дифиренциальная часть, методом 3 точек по полиному Лагранжа
        # if len(value) > 3:
        #    lp = LagrangePoly(range(len(value)), value)
        #   postvalue = lp.interpolate(len(value))
        # else:
        #   postvalue = value[len(value) - 2]
        # TODO: вот эта переменная уходит чуть ли не в бесконечность после 3-4 шагов
        # derivative = (value[len(value) - 2] - postvalue) / (2 * _timeDiscrete)
        # корявый метод переписать на выше
        # TODO:есть коряв
        if len(value) > 2:
            derivative = value[-1] - value[-2]
        else:
            derivative = 0

        return _Kp * proportional + _Ki * integral + _Kd * derivative
