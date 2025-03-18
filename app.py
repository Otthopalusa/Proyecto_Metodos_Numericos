from flask import Flask, render_template, request, redirect, url_for
from microservicios.newton_service import resolver_newton_raphson
from microservicios.punto_fijo_service import resolver_punto_fijo
from microservicios.secante_service import resolver_secante
from flask_cors import CORS

#==================================================================================================================
app = Flask(__name__)
CORS(app)

#==================================================================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/newton', methods=['GET', 'POST'])
def newton():
    if request.method == 'POST':
        ecuacion = request.form['ecuacion']
        x0 = float(request.form['x0'])
        tolerancia = float(request.form['tolerancia'])
        max_iter = int(request.form['max_iter'])
        
        resultado = resolver_newton_raphson(ecuacion, x0, tolerancia, max_iter)
        
        if 'error' in resultado:
            return render_template('newton.html', error=resultado['error'])
        else:
            return render_template('resultados.html', 
                                  metodo="Newton-Raphson",
                                  resultado=resultado,
                                  tipo_metodo="newton")
    
    return render_template('newton.html')

#==================================================================================================================
@app.route('/puntofijo', methods=['GET', 'POST'])
def punto_fijo():
    if request.method == 'POST':
        ecuacion = request.form['ecuacion']
        x0 = float(request.form['x0'])
        tolerancia = float(request.form['tolerancia'])
        max_iter = int(request.form['max_iter'])
        
        resultado = resolver_punto_fijo(ecuacion, x0, max_iter, tolerancia)
        
        if 'error' in resultado:
            return render_template('puntofijo.html', error=resultado['error'])
        else:
            return render_template('resultados.html', 
                                  metodo="Punto Fijo",
                                  resultado=resultado,
                                  tipo_metodo="puntofijo")
    
    return render_template('puntofijo.html')

#==================================================================================================================
@app.route('/secante', methods=['GET', 'POST'])
def secante():
    if request.method == 'POST':
        ecuacion = request.form['ecuacion']
        x0 = float(request.form['x0'])
        x1 = float(request.form['x1'])
        tolerancia = float(request.form['tolerancia'])
        max_iter = int(request.form['max_iter'])
        
        resultado = resolver_secante(ecuacion, x0, x1, tolerancia, max_iter)
        
        if 'error' in resultado:
            return render_template('secante.html', error=resultado['error'])
        else:
            return render_template('resultados.html', 
                                  metodo="Secante",
                                  resultado=resultado,
                                  tipo_metodo="secante")
    
    return render_template('secante.html')

#==================================================================================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)