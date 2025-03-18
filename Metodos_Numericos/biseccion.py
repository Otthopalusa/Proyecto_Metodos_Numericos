import sympy as sp

def biseccion(funcion, x, a, b, tolerancia=1e-6, max_iter=100):
    f = sp.lambdify(x, funcion)  # Convierte la función simbólica en una función evaluable

    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo no es válido. f(a) y f(b) deben tener signos opuestos.")

    iteraciones = 0
    while (b - a) / 2 > tolerancia and iteraciones < max_iter:
        c = (a + b) / 2  # Punto medio
        if f(c) == 0:
            return c, iteraciones
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iteraciones += 1

    return (a + b) / 2, iteraciones
