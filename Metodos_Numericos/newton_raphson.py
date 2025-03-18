import sympy as sp
import numpy as np

def convertir_ecuacion(ecuacion):
    # Define el símbolo de la variable
    x = sp.symbols('x')
    
    # Verifica si 'x' está en la ecuación
    if 'x' not in ecuacion:
        raise ValueError("La ecuación debe estar en términos de 'x'.")
    
    try:
        # Convierte la cadena de ecuación a una expresión simbólica
        expresion = sp.sympify(ecuacion, locals={'e': sp.E})
        
        # Simplifica la expresión
        expresion_simplificada = sp.simplify(expresion)
        
        # Devuelve una función evaluable y el símbolo 'x'
        return expresion_simplificada, x
    
    except sp.SympifyError:
        raise ValueError("La ecuación ingresada no es válida.")

def derivar_funcion(funcion, variable):
    var = sp.symbols(variable)
    func = sp.sympify(funcion)
    derivada = sp.diff(func, var)
    return derivada

def calcular_error_porcentual(valor_actual, valor_anterior):
    if valor_anterior == 0:
        return float('inf')
    else:
        return abs((valor_actual - valor_anterior) / valor_anterior) * 100

def newton_raphson(funcion, variable, x0, tolerancia=1e-6, max_iter=100):
    var = sp.symbols(variable)
    func = sp.sympify(funcion)
    derivada_func = derivar_funcion(funcion, variable)
    f = sp.lambdify(var, func, 'numpy')
    f_prime = sp.lambdify(var, derivada_func, 'numpy')
    x_n = x0
    errores = []
    for i in range(max_iter):
        f_x_n = f(x_n)
        f_prime_x_n = f_prime(x_n)
        if f_prime_x_n == 0:
            return None, errores
        x_n1 = x_n - f_x_n / f_prime_x_n
        error = calcular_error_porcentual(x_n1, x_n)
        errores.append((i+1, float(error)))
        if abs(x_n1 - x_n) < tolerancia:
            return float(x_n1), errores
        x_n = x_n1
    return None, errores