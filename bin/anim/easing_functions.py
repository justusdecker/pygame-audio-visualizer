import matplotlib.pyplot as plt
from math import pi,cos,sqrt

"""
(c) 2025 Justus Decker
"""
def animator(func) -> list[float]: return [func(i * .01) for i in range(101)]

class Animations:
    
    def linear(x: float) -> float:
        return x
    
    def heartbeat(x: float) -> float:
        E = 1.70158 * 1.525
        return [((((2 * x)**2)) * ((E + 1) * (2 * x )- E)) / 2,(((2 * x - 2)**2) * ((E + 1) * (x * 2 - 2) + E)) / 2][x > .5]

    def ease_out_back(x: float) -> float:
        C = 1.70158
        E = C - 1
        return 1 + C * ((x - 1) **3) + E * ((x - 1)**2)

    def ease_in_back(x: float) -> float:
        C = 1.70158
        E = C - 1
        return C * (x **3) - E * (x**2)

    def ease_in_out_circ(x: float) -> float:
        if x == 0: return 0
        return [((1 - sqrt(abs(1 - ((2 * x)**2)))) / 2),((sqrt(abs(1 - ((-2 * x + 2)**2))) + 1)/ 2)][x > .5]

    def ease_out_circ(x: float) -> float:
        return sqrt(1 - ((x - 1)**2))

    def ease_in_circ(x: float) -> float:
        return 1 - sqrt(1 - (x**2))

    def ease_in_out_quint(x: float) -> float:
        return [16*x*x*x*x*x,1 - ((-2 * x + 2)**5)/2][x > .5]

    def ease_out_quint(x: float) -> float:
        return 1 - ((1-x)**5)

    def ease_in_quint(x: float) -> float:
        return x**5

    def ease_in_out_quart(x: float) -> float:
        return [8*x*x*x*x,1 - ((-2 * x + 2)**4)/2][x > .5]

    def ease_out_quart(x: float) -> float:
        return 1 - ((1-x)**4)

    def ease_in_quart(x: float) -> float:
        return x**4

    def ease_in_out_cubic(x: float) -> float:
        return [4*x*x*x,1 - ((-2 * x + 2)**3)/2][x > .5]

    def ease_out_cubic(x: float) -> float:
        return 1 - ((1-x)**3)

    def ease_in_cubic(x: float) -> float:
        return x**3
    def ease_in_out_quad(x: float) -> float:
        return [2*x*x,1 - ((-2 * x + 2)**2)/2][x > .5]
    def ease_out_quad(x: float) -> float:
        return (x*-1)**2

    def ease_in_quad(x: float) -> float:
        return x**2
    def ease_out_sine(x:float) -> float:
        return cos(x*pi/2)
    def ease_in_sine(x:float) -> float:
        return 1 - cos(x*pi/2)

    def ease_out_bounce(x: float) -> float:
        N = 7.5625
        D = 2.75
        X1 = x - (1.5 / D)
        X2 = x - (2.25 / D)
        X3 = x - (2.625 / D)
        if x < 1 / D: 
            return N * (x ** 2)
        
        elif x < 2 / D: 
            x = X1
            return N * (x**2) + 0.75
        elif x < 2.5 / D: 
            x = X2
            return N * (x**2) + 0.9375
        else: 
            x = X3
            return N * (x**2) + 0.984375

plt.plot(animator(Animations.ease_in_sine))
plt.show()