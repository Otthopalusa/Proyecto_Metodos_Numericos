import sympy as sp
from utils.conversor import convertir_ecuacion, calcular_error_porcentual

#=============================================================================================================
def derivar_funcion(funcion, variable):
    """
    Calcula la derivada de una función.
    """
    var = sp.symbols(variable)
    func = sp.sympify(funcion)
    derivada = sp.diff(func, var)
    return derivada

#=============================================================================================================
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
        La raíz encontrada y una lista de errores por iteración
    """
    var = sp.symbols(variable)
    func = sp.sympify(funcion)
    derivada_func = derivar_funcion(funcion, variable)
    f = sp.lambdify(var, func, 'numpy')
    f_prime = sp.lambdify(var, derivada_func, 'numpy')
    x_n = x0
    errores = []
    valores_x = []  # Para almacenar los valores de x_n+1
    valores_fx = []  # Para almacenar f(x_n)
    valores_fpx = []  # Para almacenar f'(x_n)

    for i in range(max_iter):
        f_x_n = f(x_n)
        f_prime_x_n = f_prime(x_n)
        valores_fx.append(float(f_x_n))
        valores_fpx.append(float(f_prime_x_n))
        
        if abs(f_prime_x_n) < 1e-10:
            return None, errores, "Derivada cercana a cero. El método diverge.", valores_x, valores_fx, valores_fpx
            
        x_n1 = x_n - f_x_n / f_prime_x_n
        valores_x.append(float(x_n1))
        error = calcular_error_porcentual(x_n1, x_n)
        errores.append((i+1, float(error)))
        
        if abs(x_n1 - x_n) < tolerancia:
            return float(x_n1), errores, "Convergencia exitosa", valores_x, valores_fx, valores_fpx
            
        x_n = x_n1

    return None, errores, "Se alcanzó el número máximo de iteraciones sin convergencia", valores_x, valores_fx, valores_fpx

#========================================================================================================================================================
def resolver_newton_raphson(ecuacion_str, x0, tolerancia=1e-6, max_iter=100):
    """
    Función principal que resuelve una ecuación usando Newton-Raphson.
    """
    try:
        expresion, x = convertir_ecuacion(ecuacion_str)
        raiz, errores, mensaje, valores_x, valores_fx, valores_fpx = newton_raphson(expresion, str(x), float(x0), float(tolerancia), int(max_iter))
        return {
            'raiz': raiz,
            'errores': errores,
            'mensaje': mensaje,
            'valores_x': valores_x,
            'valores_fx': valores_fx,
            'valores_fpx': valores_fpx
        }
    except Exception as e:
        return {
            'error': str(e)
        }