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
        return sp.lambdify(x, expresion_simplificada, modules='numpy'), x
    
    except sp.SympifyError:
        raise ValueError("La ecuación ingresada no es válida.")

def calcular_error_porcentual(valor_actual, valor_anterior):
    if valor_anterior == 0:
        return float('inf')
    else:
        return abs((valor_actual - valor_anterior) / valor_anterior) * 100

def secante(f, x0, x1, tol=1e-5, max_iter=100):
    errores = []
    for i in range(max_iter):
        f_x0 = f(x0)
        f_x1 = f(x1)
        if f_x1 - f_x0 == 0:
            return None, errores
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        error = calcular_error_porcentual(x2, x1)
        errores.append((i+1, float(error)))
        if abs(x2 - x1) < tol:
            return float(x2), errores
        x0 = x1
        x1 = x2
    return None, errores