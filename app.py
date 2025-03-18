from flask import Flask, render_template, request, jsonify
from Metodos_Numericos.newton_raphson import newton_raphson, convertir_ecuacion as convertir_ecuacion_newton
from Metodos_Numericos.secante import secante, convertir_ecuacion as convertir_ecuacion_secante
from Metodos_Numericos.punto_fijo import punto_fijo


app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)