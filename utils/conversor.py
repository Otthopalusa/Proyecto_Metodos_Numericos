import sympy as sp

#===============================================================================
def convertir_ecuacion(ecuacion):
    """
    Convierte una cadena de texto a una expresión simbólica de sympy.
    """
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
        return expresion_simplificada, x
    
    except sp.SympifyError:
        raise ValueError("La ecuación ingresada no es válida.")

#===============================================================================
def calcular_error_porcentual(valor_actual, valor_anterior):
    """
    Calcula el error porcentual entre dos valores.
    """
    if abs(valor_anterior) < 1e-10:
        return float('inf')
    else:
        return abs((valor_actual - valor_anterior) / valor_anterior) * 100