import sympy as sp
from utils.conversor import convertir_ecuacion, calcular_error_porcentual

#=======================================================================================================================
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
        La raíz encontrada y una lista con los datos de cada iteración
    """
    x_actual = float(valor_inicial)
    f = sp.lambdify(x, ecuacion, 'numpy')
    
    # Lista para almacenar los datos de cada iteración
    iteraciones = []
    
    for i in range(1, max_iter + 1):
        x_anterior = x_actual
        
        # Calcular g(x)
        g_x = float(f(x_anterior))  
        x_actual = g_x
        
        error = calcular_error_porcentual(x_actual, x_anterior)
        
        # Guardar datos de la iteración actual
        iteraciones.append({
            'iteracion': i,
            'x_n': x_anterior,
            'g_x_n': g_x,
            'error': error
        })
        
        if error < tolerancia:
            mensaje = "Convergencia exitosa"
            return x_actual, iteraciones, mensaje

    mensaje = "Se alcanzó el número máximo de iteraciones sin convergencia"
    return None, iteraciones, mensaje

#=======================================================================================================================
def resolver_punto_fijo(ecuacion_str, valor_inicial, max_iter=100, tolerancia=1e-4):
    """
    Función principal que resuelve una ecuación usando punto fijo.
    """
    try:
        expr, x = convertir_ecuacion(ecuacion_str)
        
        # En punto fijo, necesitamos convertir la ecuación f(x) = 0 a la forma x = g(x)
        # Despejamos para obtener g(x) = x - f(x)
        g_x = x - expr  # Esta es una forma de despejar, hay otras
        
        raiz, iteraciones, mensaje = punto_fijo(g_x, x, float(valor_inicial), int(max_iter), float(tolerancia))
        
        return {
            'raiz': raiz,
            'iteraciones': iteraciones,
            'mensaje': mensaje,
            'ecuacion_original': str(expr),
            'ecuacion_despejada': str(g_x)
        }
    except Exception as e:
        return {
            'error': str(e)
        }