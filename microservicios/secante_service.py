import sympy as sp
import numpy as np
from utils.conversor import convertir_ecuacion, calcular_error_porcentual

#===========================================================================================================
def secante(ecuacion, x, x0, x1, tol=1e-5, max_iter=100):
    """
    Implementa el método de la secante para encontrar raíces.
    
    Args:
        ecuacion: Expresión simbólica de la ecuación
        x: Variable de la función (símbolo)
        x0: Primer valor inicial
        x1: Segundo valor inicial
        tol: Tolerancia para el criterio de parada
        max_iter: Número máximo de iteraciones
        
    Returns:
        La raíz encontrada y una lista con los datos de cada iteración
    """
    f = sp.lambdify(x, ecuacion, 'numpy')
    
    # Lista para almacenar los datos de cada iteración
    iteraciones = []
    
    for i in range(max_iter):
        f_x0 = float(f(x0))
        f_x1 = float(f(x1))
        
        if abs(f_x1 - f_x0) < 1e-10:
            mensaje = "División por cero. Método divergente."
            return None, iteraciones, mensaje
            
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        error = calcular_error_porcentual(x2, x1)
        
        # Guardar datos de la iteración actual
        iteraciones.append({
            'iteracion': i + 1,
            'x0': x0,
            'x1': x1,
            'f_x0': f_x0,
            'f_x1': f_x1,
            'x2': x2,
            'error': error
        })
        
        if abs(x2 - x1) < tol:
            mensaje = "Convergencia exitosa"
            return float(x2), iteraciones, mensaje
            
        x0 = x1
        x1 = x2
        
    mensaje = "Se alcanzó el número máximo de iteraciones sin convergencia"
    return None, iteraciones, mensaje

#===========================================================================================================
def resolver_secante(ecuacion_str, x0, x1, tolerancia=1e-5, max_iter=100):
    """
    Función principal que resuelve una ecuación usando el método de la secante.
    """
    try:
        expr, x = convertir_ecuacion(ecuacion_str)
        
        raiz, iteraciones, mensaje = secante(expr, x, float(x0), float(x1), float(tolerancia), int(max_iter))
        
        return {
            'raiz': raiz,
            'iteraciones': iteraciones,
            'mensaje': mensaje,
            'ecuacion': str(expr)
        }
    except Exception as e:
        return {
            'error': str(e)
        }