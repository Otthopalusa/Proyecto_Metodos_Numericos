import numpy as np
import sympy as sp

def biseccion(ecuacion, a, b, tolerancia=1e-6, max_iter=100):
    """
    Implementación del método de bisección para encontrar raíces de una ecuación.
    
    Parámetros:
    ecuacion -- ecuación en forma de cadena para encontrar su raíz
    a -- límite inferior del intervalo
    b -- límite superior del intervalo
    tolerancia -- criterio de parada (por defecto 1e-6)
    max_iter -- número máximo de iteraciones (por defecto 100)
    
    Retorna:
    Un diccionario con:
    - success: indica si el método encontró una raíz
    - raiz: la raíz encontrada (si success es True)
    - message: mensaje informativo o de error
    - iteraciones: lista de diccionarios con la información de cada iteración
    - intervalo_final: intervalo final [a, b]
    """
    try:
        # Preparar la función
        x = sp.Symbol('x')
        f_expr = sp.sympify(ecuacion)
        f = sp.lambdify(x, f_expr, modules=['numpy', {'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'log': np.log}])
        
        # Verificar que hay un cambio de signo en el intervalo
        fa = float(f(a))
        fb = float(f(b))
        
        if fa * fb > 0:
            return {
                'success': False,
                'message': f"No hay cambio de signo en el intervalo [{a}, {b}]. El método de bisección requiere f(a) y f(b) de signos opuestos.",
                'iteraciones': []
            }
        
        # Lista para almacenar las iteraciones
        iteraciones = []
        
        # Iteraciones del método
        iter_count = 0
        error = float('inf')
        c_anterior = None
        
        while error > tolerancia and iter_count < max_iter:
            # Calcular punto medio
            c = (a + b) / 2
            fc = float(f(c))
            
            # Guardar información de la iteración
            iter_info = {
                'iteracion': iter_count + 1,
                'a': a,
                'b': b,
                'c': c,
                'f_a': fa,
                'f_b': fb,
                'f_c': fc,
                'error': error if c_anterior is not None else "N/A"
            }
            iteraciones.append(iter_info)
            
            # Verificar si hemos encontrado la raíz
            if abs(fc) < tolerancia:
                return {
                    'success': True,
                    'raiz': c,
                    'message': f"Se encontró una raíz con la tolerancia requerida en {iter_count + 1} iteraciones.",
                    'iteraciones': iteraciones,
                    'intervalo_final': [a, b]
                }
            
            # Actualizar el intervalo según el cambio de signo
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
            
            # Calcular error si tenemos un punto anterior
            if c_anterior is not None:
                error = abs(c - c_anterior)
            c_anterior = c
            
            iter_count += 1
        
        # Verificar si se alcanzó la convergencia
        if iter_count >= max_iter:
            return {
                'success': False,
                'message': f"Se alcanzó el número máximo de iteraciones ({max_iter}) sin converger a la tolerancia requerida.",
                'iteraciones': iteraciones,
                'intervalo_final': [a, b],
                'ultima_aproximacion': c
            }
        
        return {
            'success': True,
            'raiz': c,
            'message': f"Se encontró una raíz con la tolerancia requerida en {iter_count} iteraciones.",
            'iteraciones': iteraciones,
            'intervalo_final': [a, b]
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Error: {str(e)}",
            'iteraciones': []
        }