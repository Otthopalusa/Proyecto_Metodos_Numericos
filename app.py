from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
import numpy as np
import sympy as sp
from Metodos_Numericos.newton_raphson import newton_raphson, convertir_ecuacion as convertir_ecuacion_newton
from Metodos_Numericos.secante import secante, convertir_ecuacion as convertir_ecuacion_secante
from Metodos_Numericos.punto_fijo import punto_fijo
from Metodos_Numericos.biseccion import biseccion
from Metodos_Numericos.jacobi import jacobi



app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Rutas de otros métodos numéricos (omito por brevedad)
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
        ecuacion = request.form.get('ecuacion')
        g_x = request.form.get('g_x')
        x0 = float(request.form.get('x0'))
        tolerancia = float(request.form.get('tolerancia', '1e-6'))
        max_iter = int(request.form.get('max_iter', '100'))
        
        resultado = punto_fijo(ecuacion, g_x, x0, tolerancia, max_iter)
        
        return render_template('resultados.html', metodo="Punto Fijo", ecuacion=ecuacion, resultado=resultado, tipo="punto_fijo")
    except Exception as e:
        return render_template('resultados.html', metodo="Punto Fijo", error=str(e), tipo="punto_fijo")
    

@app.route('/calcular_biseccion', methods=['POST'])
def calcular_biseccion():
    try:
        ecuacion_str = request.form['ecuacion']
        a = float(request.form['a'])
        b = float(request.form['b'])
        tolerancia = float(request.form['tolerancia'])
        max_iter = int(request.form['max_iter'])

        x = sp.Symbol('x')
        ecuacion = sp.sympify(ecuacion_str)  # Convierte la ecuación en una función simbólica

        raiz, iteraciones = biseccion(ecuacion, x, a, b, tolerancia, max_iter)

        resultado = f"La raíz encontrada es {raiz:.6f} después de {iteraciones} iteraciones."
    except Exception as e:
        resultado = f"Error: {e}"

    return render_template('index.html', resultado=resultado)
 
@app.route('/jacobi')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
