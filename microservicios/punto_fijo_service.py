import sympy as sp
from utils.conversor import convertir_ecuacion, calcular_error_porcentual

#=========================================================================================================================================
def complex_to_dict(c):
    """
    Convierte un número complejo a un diccionario con partes real e imaginaria.
    """
    return {'real': float(c.real), 'imag': float(c.imag)}

#=========================================================================================================================================
def punto_fijo(ecuacion, x, valor_inicial, max_iter=100, tolerancia=1e-4):
    """
    Implementa el método de punto fijo para encontrar raíces.
    
    Args:
        ecuacion: Expresión simbólica de la ecuación de punto fijo
        x: Variable de la función (símbolo)
        valor_inicial: Valor inicial
        max_iter: Número máximo de iteraciones
        tolerancia: Tolerancia para el criterio de parada
    
    Returns:
        La raíz encontrada y una lista de errores por iteración
    """
    iteraciones = []
    aproximaciones = [complex(valor_inicial)]
    errores = []
    x_actual = complex(valor_inicial)

    for i in range(1, max_iter + 1):
        x_anterior = x_actual
        x_actual = complex(ecuacion.subs(x, x_anterior).evalf())
        aproximaciones.append(x_actual)
        error_actual = calcular_error_porcentual(x_actual, x_anterior)
        
        iteraciones.append(i)
        errores.append((i, float(error_actual)))

        if error_actual < tolerancia:
            return complex_to_dict(x_actual), errores, "Convergencia exitosa", aproximaciones

    return None, errores, "Se alcanzó el número máximo de iteraciones sin convergencia", aproximaciones

#=========================================================================================================================================
def resolver_punto_fijo(ecuacion_str, valor_inicial, max_iter=100, tolerancia=1e-4):
    """
    Función principal que resuelve una ecuación usando punto fijo.
    """
    try:
        ecuacion, x = convertir_ecuacion(ecuacion_str)
        
        # Convertir la función a la forma de punto fijo g(x) = x
        # Para ello despejamos g(x) = x + f(x)
        g_x = ecuacion + x
        
        raiz, errores, mensaje, aproximaciones = punto_fijo(g_x, x, float(valor_inicial), int(max_iter), float(tolerancia))
        
        return {
            'raiz': raiz,
            'errores': errores,
            'mensaje': mensaje,
            'aproximaciones': aproximaciones
        }
    except Exception as e:
        return {
            'error': str(e)
        }