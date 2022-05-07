from PID.Lagrange import LagrangePoly

_setPoint = 0
_Kp = 1
_Ki = 1
_Kd = 1

_timeDiscrete = 1


class PID:
    global _setPoint, _Ki, _Kp, _Kd

    def __init__(self, Kp, Ki, Kd, setpoint):
        global _setPoint, _Ki, _Kp, _Kd
        _setPoint = setpoint
        _Kd = Kd
        _Ki = Ki
        _Kp = Kp

    @staticmethod
    def getControlAction(value):
        global _Ki, _Kp, _Kd
        # Пропорциональная
        proportional = (_setPoint - value[-1])
        # Интегральная часть, по методу трапеции
        integral = 0
        for it in range(1, len(value)):
            trapezoidArea = 1 / 2 * (value[it] + value[it]) * _timeDiscrete
            integral += trapezoidArea
        # Дифиренциальная часть, методом 3 точек по полиному Лагранжа
        if len(value) > 3:
            lp = LagrangePoly(range(len(value)), value)
            postvalue = lp.interpolate(len(value))
        else:
            postvalue = value[len(value) - 2]
        derivative = (value[len(value) - 2] - postvalue) / (2 * _timeDiscrete)
        return _Kp * proportional + _Ki * integral + _Kd * derivative
