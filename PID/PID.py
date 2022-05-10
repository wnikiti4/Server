from PID.Lagrange import LagrangePoly

_setPoint = 0
_Kp = 1.0
_Ki = 1.0
_Kd = 1.0

_timeDiscrete = 1.0


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
        proportional :float = (_setPoint - value[-1])
        # Интегральная часть, по методу трапеции
        integral = 0.0
        for it in range(1, len(value)):
            trapezoidArea = 1 / 2 * (value[it] + value[it]) * _timeDiscrete
            integral += trapezoidArea
        # Дифиренциальная часть, методом 3 точек по полиному Лагранжа
        if len(value) > 3:
            lp = LagrangePoly(range(len(value)), value)
            postvalue = lp.interpolate(len(value))
        else:
            postvalue = value[len(value) - 2]
        derivative: float = (value[len(value) - 2] - postvalue) / (2 * _timeDiscrete)
        return float(_Kp) * float(proportional) + float(_Ki) * float(integral) + float(_Kd) * float(derivative)
