from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
import numpy as np
import sympy as sp
from Metodos_Numericos.newton_raphson import newton_raphson, convertir_ecuacion as convertir_ecuacion_newton
from Metodos_Numericos.secante import secante, convertir_ecuacion as convertir_ecuacion_secante
from Metodos_Numericos.biseccion import biseccion
from Metodos_Numericos.jacobi import jacobi
from Metodos_Numericos.gauss_seidel import gauss_seidel

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Función de punto fijo implementada directamente en app.py
def punto_fijo(ecuacion_str, g_x_str, x0, tolerancia=1e-6, max_iter=100):
    try:
        x = sp.Symbol('x')
        
        # Convertir a expresiones simbólicas
        g_expr = sp.sympify(g_x_str)
        
        # Crear función lambda para evaluación numérica
        g_func = sp.lambdify(x, g_expr)
        
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

# Función para el método jacobi
def jacobi(A, b, x0, tol=1e-6, max_iter=100):
    n = len(b)
    x = x0.copy()
    x_new = x.copy()
    
    for k in range(max_iter):
        for i in range(n):
            sum_ax = 0
            for j in range(n):
                if i != j:
                    sum_ax += A[i, j] * x[j]
            
            x_new[i] = (b[i] - sum_ax) / A[i, i]
        
        # Calcular el error y verificar convergencia
        error = np.linalg.norm(x_new - x)
        if error < tol:
            return x_new
        
        # Actualizar x para la siguiente iteración
        x = x_new.copy()
    
    return None

# Rutas de otros métodos numéricos
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/newton_raphson')
def newton_raphson_form():
    return render_template('newton_raphson.html')

@app.route('/secante')
def secante_form():
    return render_template('secante.html')

@app.route('/punto_fijo')
def punto_fijo_form():
    return render_template('punto_fijo.html')

@app.route('/biseccion')
def biseccion_page():
    return render_template('biseccion.html')

@app.route('/calcular_newton_raphson', methods=['POST'])
def calcular_newton_raphson():
    try:
        ecuacion = request.form.get('ecuacion')
        x0 = float(request.form.get('x0'))
        tolerancia = float(request.form.get('tolerancia', '1e-6'))
        max_iter = int(request.form.get('max_iter', '100'))
        
        raiz, iteraciones = newton_raphson(ecuacion, 'x', x0, tolerancia, max_iter)
        
        if raiz is None:
            resultado = {
                "success": False,
                "message": "El método no convergió",
                "iteraciones": iteraciones
            }
        else:
            resultado = {
                "success": True,
                "raiz": raiz,
                "iteraciones": iteraciones
            }
        
        return render_template('resultados.html', 
                              metodo="Newton-Raphson", 
                              ecuacion=ecuacion,
                              resultado=resultado,
                              tipo="newton_raphson")
    except Exception as e:
        return render_template('resultados.html', 
                              metodo="Newton-Raphson", 
                              error=str(e),
                              tipo="newton_raphson")

@app.route('/calcular_secante', methods=['POST'])
def calcular_secante():
    try:
        ecuacion = request.form.get('ecuacion')
        x0 = float(request.form.get('x0'))
        x1 = float(request.form.get('x1'))
        tolerancia = float(request.form.get('tolerancia', '1e-5'))
        max_iter = int(request.form.get('max_iter', '100'))
        
        f, _ = convertir_ecuacion_secante(ecuacion)
        raiz, iteraciones = secante(f, x0, x1, tolerancia, max_iter)
        
        if raiz is None:
            resultado = {
                "success": False,
                "message": "El método no convergió",
                "iteraciones": iteraciones
            }
        else:
            resultado = {
                "success": True,
                "raiz": raiz,
                "iteraciones": iteraciones
            }
        
        return render_template('resultados.html', 
                              metodo="Secante", 
                              ecuacion=ecuacion,
                              resultado=resultado,
                              tipo="secante")
    except Exception as e:
        return render_template('resultados.html', 
                              metodo="Secante", 
                              error=str(e),
                              tipo="secante")
    
@app.route('/calcular_punto_fijo', methods=['POST'])
def calcular_punto_fijo():
    try:
        ecuacion = request.form.get('ecuacion', '')
        g_x = request.form.get('g_x')
        x0 = float(request.form.get('x0'))
        tolerancia = float(request.form.get('tolerancia', '1e-6'))
        max_iter = int(request.form.get('max_iter', '100'))
        
        # Implementación que maneja mejor errores numéricos
        import sympy as sp
        import numpy as np
        
        x = sp.Symbol('x')
        g_expr = sp.sympify(g_x)
        g_func = sp.lambdify(x, g_expr, modules=['numpy', {'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'log': np.log}])
        
        iteraciones = []
        x_actual = float(x0)
        convergio = False
        raiz = None
        mensaje = ""
        
        for i in range(max_iter):
            try:
                # Verificar si el valor actual es demasiado grande
                if abs(x_actual) > 1e100:
                    mensaje = f"El valor de x se volvió demasiado grande en la iteración {i+1}. El método está divergiendo."
                    break
                
                # Calcular nuevo valor con manejo de excepciones
                x_nuevo = float(g_func(x_actual))
                
                # Verificar si el resultado es un número válido
                if not np.isfinite(x_nuevo):
                    mensaje = f"La iteración produjo un valor no finito en la iteración {i+1}. La función probablemente diverge."
                    break
                
                # Calcular error
                error = abs(x_nuevo - x_actual)
                
                # Guardar esta iteración
                iteraciones.append((i+1, x_actual, x_nuevo, error))
                
                # Verificar convergencia
                if error < tolerancia:
                    convergio = True
                    raiz = x_nuevo
                    break
                
                # Verificar si el error está aumentando (divergencia)
                if i > 0 and error > 10 * iteraciones[-2][3]:  # Error aumenta muy rápido
                    mensaje = f"El error está aumentando rápidamente en la iteración {i+1}. El método parece estar divergiendo."
                    break
                
                # Actualizar para próxima iteración
                x_actual = x_nuevo
                
            except OverflowError:
                mensaje = f"Desbordamiento numérico en la iteración {i+1}. Los valores se volvieron demasiado grandes."
                break
            except Exception as e:
                mensaje = f"Error en la iteración {i+1}: {str(e)}"
                break
        
        # Si se alcanzó el máximo de iteraciones sin convergir
        if not convergio and not mensaje:
            mensaje = f"No se alcanzó la convergencia después de {max_iter} iteraciones"
        
        # Renderizar plantilla
        return render_template('resultados_punto_fijo.html',
                              ecuacion=g_x,
                              iteraciones=iteraciones,
                              convergio=convergio,
                              raiz=raiz,
                              mensaje=mensaje)
                              
    except Exception as e:
        # Error general
        return render_template('resultados_punto_fijo.html',
                              ecuacion=g_x if 'g_x' in locals() else "",
                              error=str(e))
@app.route('/calcular_biseccion', methods=['POST'])
def calcular_biseccion():
    try:
        ecuacion = request.form.get('ecuacion', '')
        a = float(request.form.get('a'))
        b = float(request.form.get('b'))
        tolerancia = float(request.form.get('tolerancia', '1e-6'))
        max_iter = int(request.form.get('max_iter', '100'))
        
        # Llamar a la función biseccion
        from Metodos_Numericos.biseccion import biseccion
        resultado = biseccion(ecuacion, a, b, tolerancia, max_iter)
        
        return render_template('resultados.html', 
                              metodo="Bisección",
                              ecuacion=ecuacion,
                              resultado=resultado,
                              tipo="biseccion")
                              
    except Exception as e:
        return render_template('resultados.html',
                              metodo="Bisección",
                              ecuacion=ecuacion if 'ecuacion' in locals() else "",
                              error=str(e),
                              tipo="biseccion")
def jacobi_form():
    return render_template('jacobi.html')

# Endpoint para calcular Jacobi (lee datos como JSON)
@app.route('/calcular_jacobi', methods=['POST'])
def calcular_jacobi():
    try:
        data = request.get_json()  # Leer los datos en formato JSON
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        # Verifica que se haya enviado el campo 'matrix_size'
        if data.get('matrix_size') is None:
            return jsonify({"error": "Falta el campo matrix_size"}), 400
        matrix_size = int(data.get('matrix_size'))
        
        A_str = data.get('A')
        b_str = data.get('b')
        x0_str = data.get('x0')
        tolerancia = float(data.get('tolerancia', 1e-6))
        max_iter = int(data.get('max_iter', 100))
        
        # Convertir la cadena de la matriz A (filas separadas por ';' y elementos por ',')
        A_rows = A_str.split(';')
        A = [list(map(float, row.split(','))) for row in A_rows]
        A = np.array(A)
        b = np.array(list(map(float, b_str.split(','))))
        x0 = np.array(list(map(float, x0_str.split(','))))
        
        # Llamar a la función jacobi importada
        result = jacobi(A, b, x0, tolerancia, max_iter)
        if result is None:
            resultado = {"success": False, "message": "No se alcanzó la tolerancia deseada", "iteraciones": max_iter}
        else:
            resultado = {"success": True, "resultado": result.tolist()}
            
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def jacobi_form():
    return render_template('gauss_seidel.html')

# Endpoint para calcular Jacobi (lee datos como JSON)
@app.route('/calcular_gauss_seidel', methods=['POST'])
def calcular_gauss_seidel():
    try:
        data = request.get_json()  # Leer los datos en formato JSON
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        # Verifica que se haya enviado el campo 'matrix_size'
        if data.get('matrix_size') is None:
            return jsonify({"error": "Falta el campo matrix_size"}), 400
        matrix_size = int(data.get('matrix_size'))
        
        A_str = data.get('A')
        b_str = data.get('b')
        x0_str = data.get('x0')
        tolerancia = float(data.get('tolerancia', 1e-6))
        max_iter = int(data.get('max_iter', 100))
        
        # Convertir la cadena de la matriz A (filas separadas por ';' y elementos por ',')
        A_rows = A_str.split(';')
        A = [list(map(float, row.split(','))) for row in A_rows]
        A = np.array(A)
        b = np.array(list(map(float, b_str.split(','))))
        x0 = np.array(list(map(float, x0_str.split(','))))
        
        # Llamar a la función jacobi importada
        result = gauss_seidel(A, b, x0, tolerancia, max_iter)
        if result is None:
            resultado = {"success": False, "message": "No se alcanzó la tolerancia deseada", "iteraciones": max_iter}
        else:
            resultado = {"success": True, "resultado": result.tolist()}
            
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)