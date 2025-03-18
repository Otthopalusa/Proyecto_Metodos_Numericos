import sympy as sp
import numpy as np
from utils.conversor import convertir_ecuacion, calcular_error_porcentual

#=====================================================================================================================================
def secante(funcion, x0, x1, tol=1e-5, max_iter=100):
    """
    Implementa el método de la secante para encontrar raíces.
    
    Args:
        funcion: Función lambda de la ecuación
        x0: Primer valor inicial
        x1: Segundo valor inicial
        tol: Tolerancia para el criterio de parada
        max_iter: Número máximo de iteraciones
        
    Returns:
        La raíz encontrada y una lista de errores por iteración
    """
    errores = []
    valores_x = [float(x0), float(x1)]
    valores_fx = [float(funcion(x0)), float(funcion(x1))]
    
    for i in range(max_iter):
        f_x0 = funcion(x0)
        f_x1 = funcion(x1)
        
        if abs(f_x1 - f_x0) < 1e-10:
            return None, errores, "División por cero. Método divergente.", valores_x, valores_fx
            
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        valores_x.append(float(x2))
        valores_fx.append(float(funcion(x2)))
        
        error = calcular_error_porcentual(x2, x1)
        errores.append((i+1, float(error)))
        
        if abs(x2 - x1) < tol:
            return float(x2), errores, "Convergencia exitosa", valores_x, valores_fx
            
        x0 = x1
        x1 = x2
        
    return None, errores, "Se alcanzó el número máximo de iteraciones sin convergencia", valores_x, valores_fx

#=====================================================================================================================================
def resolver_secante(ecuacion_str, x0, x1, tolerancia=1e-5, max_iter=100):
    """
    Función principal que resuelve una ecuación usando el método de la secante.
    """
    try:
        expr, x = convertir_ecuacion(ecuacion_str)
        func = sp.lambdify(x, expr, 'numpy')
        
        raiz, errores, mensaje, valores_x, valores_fx = secante(func, float(x0), float(x1), float(tolerancia), int(max_iter))
        
        return {
            'raiz': raiz,
            'errores': errores,
            'mensaje': mensaje,
            'valores_x': valores_x,
            'valores_fx': valores_fx
        }
    except Exception as e:
        return {
            'error': str(e)
        }