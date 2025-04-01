import sympy as sp
import numpy as np

def punto_fijo(ecuacion_str, g_x_str, x0, tolerancia=1e-6, max_iter=100):
    """
    Implementa el método de punto fijo para encontrar raíces de ecuaciones.
    
    Parámetros:
    ecuacion_str: String con la ecuación cuya raíz se busca (no se utiliza directamente, pero es útil tenerla)
    g_x_str: String con la función g(x) que se utilizará para iterar
    x0: Valor inicial
    tolerancia: Tolerancia para la convergencia
    max_iter: Número máximo de iteraciones
    
    Retorno:
    Un diccionario con los resultados del método
    """
    try:
        x = sp.Symbol('x')
        
        # Convertir a expresiones simbólicas
        g_expr = sp.sympify(g_x_str)
        
        # Crear función lambda para evaluación numérica
        g_func = sp.lambdify(x, g_expr, modules=['numpy', {'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'log': np.log}])
        
        iteraciones = []
        
        # Valor inicial
        x_actual = float(x0)
        
        for i in range(max_iter):
            try:
                # Calcular próximo valor
                x_siguiente = float(g_func(x_actual))
                
                # Verificar que sea un número válido
                if not np.isfinite(x_siguiente):
                    return {
                        'success': False,
                        'message': f"La iteración produjo un valor no válido en la iteración {i+1}",
                        'iteraciones': iteraciones
                    }
                
                # Calcular error
                error = abs(x_siguiente - x_actual)
                
                # Guardar datos de esta iteración
                iteraciones.append({
                    'iteracion': i + 1,
                    'x0': float(x_actual),
                    'x1': float(x_siguiente),
                    'error': float(error)
                })
                
                # Verificar convergencia
                if error < tolerancia:
                    return {
                        'success': True,
                        'raiz': float(x_siguiente),
                        'iteraciones': iteraciones
                    }
                
                # Verificar si está divergiendo (valores muy grandes)
                if abs(x_siguiente) > 1e10:
                    return {
                        'success': False,
                        'message': f"La iteración está divergiendo. Valor actual: {x_siguiente}",
                        'iteraciones': iteraciones
                    }
                
                # Actualizar para próxima iteración
                x_actual = x_siguiente
                
            except Exception as e:
                return {
                    'success': False,
                    'message': f"Error en la iteración {i+1}: {str(e)}",
                    'iteraciones': iteraciones
                }
        
        # Si llegamos aquí, es porque se alcanzó el máximo de iteraciones
        return {
            'success': False,
            'message': f"No se alcanzó la convergencia después de {max_iter} iteraciones.",
            'iteraciones': iteraciones
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Error al inicializar el método: {str(e)}",
            'iteraciones': []
        }

def verificar_convergencia(g_x_str, x_aprox, tolerancia=1e-5):
    """
    Función auxiliar para verificar si el método de punto fijo convergerá.
    Calcula |g'(x)| y verifica si es menor que 1 para garantizar convergencia.
    
    Parámetros:
    g_x_str: String con la función g(x)
    x_aprox: Valor aproximado de la raíz
    tolerancia: Tolerancia para evaluar
    
    Retorno:
    bool: True si es probable que converja, False en caso contrario
    """
    try:
        x = sp.Symbol('x')
        g_expr = sp.sympify(g_x_str)
        
        # Derivada de g(x)
        g_prime = sp.diff(g_expr, x)
        
        # Convertir a función evaluable
        g_prime_func = sp.lambdify(x, g_prime)
        
        # Evaluar en x_aprox
        valor_derivada = abs(float(g_prime_func(x_aprox)))
        
        # Si |g'(x)| < 1, es probable que converja
        return valor_derivada < 1
    except:
        # Si hay error, no podemos asegurar convergencia
        return False