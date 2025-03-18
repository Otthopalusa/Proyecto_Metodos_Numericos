import sympy as sp
from utils.conversor import convertir_ecuacion, calcular_error_porcentual

#===========================================================================================================
def derivar_funcion(funcion, variable):
    """
    Calcula la derivada de una función.
    """
    var = sp.symbols(variable)
    func = sp.sympify(funcion)
    derivada = sp.diff(func, var)
    return derivada

#===========================================================================================================
def newton_raphson(funcion, variable, x0, tolerancia=1e-6, max_iter=100):
    """
    Implementa el método de Newton-Raphson para encontrar raíces.
    
    Args:
        funcion: Expresión simbólica de la función
        variable: Variable de la función (símbolo)
        x0: Valor inicial
        tolerancia: Tolerancia para el criterio de parada
        max_iter: Número máximo de iteraciones
        
    Returns:
        La raíz encontrada y una lista de iteraciones con valores y errores
    """
    var = sp.symbols(variable)
    func = sp.sympify(funcion)
    derivada_func = derivar_funcion(funcion, variable)
    f = sp.lambdify(var, func, 'numpy')
    f_prime = sp.lambdify(var, derivada_func, 'numpy')
    x_n = float(x0)
    
    # Lista para almacenar los datos de cada iteración
    iteraciones = []
    
    for i in range(max_iter):
        f_x_n = float(f(x_n))
        f_prime_x_n = float(f_prime(x_n))
        
        if abs(f_prime_x_n) < 1e-10:
            mensaje = "Derivada cercana a cero. El método diverge."
            return None, iteraciones, mensaje
            
        x_n1 = x_n - f_x_n / f_prime_x_n
        error = calcular_error_porcentual(x_n1, x_n)
        
        # Guardar datos de la iteración actual
        iteraciones.append({
            'iteracion': i + 1,
            'x_n': x_n,
            'f_x_n': f_x_n,
            'f_prima_x_n': f_prime_x_n,
            'x_n1': x_n1,
            'error': error
        })
        
        if abs(x_n1 - x_n) < tolerancia:
            mensaje = "Convergencia exitosa"
            return float(x_n1), iteraciones, mensaje
            
        x_n = x_n1

    return None, iteraciones, "Se alcanzó el número máximo de iteraciones sin convergencia"

#===========================================================================================================
def resolver_newton_raphson(ecuacion_str, x0, tolerancia=1e-6, max_iter=100):
    """
    Función principal que resuelve una ecuación usando Newton-Raphson.
    """
    try:
        expresion, x = convertir_ecuacion(ecuacion_str)
        raiz, iteraciones, mensaje = newton_raphson(expresion, str(x), x0, tolerancia, max_iter)
        
        return {
            'raiz': raiz,
            'iteraciones': iteraciones,
            'mensaje': mensaje,
            'ecuacion': str(expresion),
            'derivada': str(derivar_funcion(expresion, str(x)))
        }
    except Exception as e:
        return {
            'error': str(e)
        }