import sympy as sp
import numpy as np

#====================================================================================================================
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

#====================================================================================================================
def calcular_error_porcentual(valor_actual, valor_anterior):
    if valor_anterior == 0:
        return float('inf')
    else:
        return abs((valor_actual - valor_anterior) / valor_anterior) * 100

#====================================================================================================================
def secante(f, x0, x1, tol=1e-5, max_iter=100):
    iteraciones = []
    
    # Agregar los valores iniciales
    f_x0 = f(x0)
    f_x1 = f(x1)
    
    # Primer punto (no hay error aún)
    iteraciones.append({
        "iteracion": 0,
        "valor": float(x0),
        "f_x": float(f_x0),
        "error_porcentual": "N/A"
    })
    
    # Segundo punto (calculamos error respecto al primero)
    error_inicial = calcular_error_porcentual(x1, x0)
    iteraciones.append({
        "iteracion": 1,
        "valor": float(x1),
        "f_x": float(f_x1),
        "error_porcentual": float(error_inicial)
    })
    
    for i in range(max_iter):
        if f_x1 - f_x0 == 0:
            return None, iteraciones
            
        # Calcular el nuevo valor
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = f(x2)
        
        # Calcular el error
        error = calcular_error_porcentual(x2, x1)
        
        # Guardar la información de la iteración
        iteraciones.append({
            "iteracion": i+2,  # +2 porque ya tenemos dos puntos iniciales
            "valor": float(x2),
            "f_x": float(f_x2),
            "error_porcentual": float(error)
        })
        
        # Verificar convergencia
        if abs(x2 - x1) < tol:
            return float(x2), iteraciones

        # Actualizar valores para la siguiente iteración
        x0 = x1
        x1 = x2
        f_x0 = f_x1
        f_x1 = f_x2
    
    return None, iteraciones