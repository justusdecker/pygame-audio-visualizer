import matplotlib.pyplot as plt

def animator(func) -> list[float]:
    return [func(i * .01) for i in range(101)]
def easy_out_bounce(x: int) -> float:
    """
    Code converted from: https://easings.net/de#easeOutBounce
    """
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

plt.plot(animator(easy_out_bounce))
plt.show()