document.addEventListener("DOMContentLoaded", function() {
    // Referencias a los elementos del DOM
    const form = document.getElementById('jacobiForm');
    const matrixSizeInput = document.getElementById('matrixSize');
    const matrixAContainer = document.getElementById('matrixA');
    const vectorBContainer = document.getElementById('vectorB');
    const vectorX0Container = document.getElementById('vectorX0');
    const resultContainer = document.getElementById('result');
  
    // Inicializa el formulario con tamaño por defecto 3
    let matrixSize = parseInt(matrixSizeInput.value);
    renderInputs(matrixSize);
  
    // Actualiza los campos cada vez que se cambia el tamaño de la matriz
    matrixSizeInput.addEventListener('change', function(e) {
      matrixSize = parseInt(e.target.value);
      renderInputs(matrixSize);
    });
  
    // Función para generar los inputs para la matriz A y vectores b y x0
    function renderInputs(size) {
      // Genera inputs para la matriz A (NxN)
      matrixAContainer.innerHTML = '';
      for (let i = 0; i < size; i++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'matrix-row';
        for (let j = 0; j < size; j++) {
          const input = document.createElement('input');
          input.type = 'number';
          input.value = 0;
          input.required = true;
          input.style.margin = '2px';
          rowDiv.appendChild(input);
        }
        matrixAContainer.appendChild(rowDiv);
      }
  
      // Genera inputs para el vector b (tamaño N)
      vectorBContainer.innerHTML = '';
      for (let i = 0; i < size; i++) {
        const input = document.createElement('input');
        input.type = 'number';
        input.value = 0;
        input.required = true;
        input.style.margin = '2px';
        vectorBContainer.appendChild(input);
      }
  
      // Genera inputs para el vector x0 (tamaño N)
      vectorX0Container.innerHTML = '';
      for (let i = 0; i < size; i++) {
        const input = document.createElement('input');
        input.type = 'number';
        input.value = 0;
        input.required = true;
        input.style.margin = '2px';
        vectorX0Container.appendChild(input);
      }
    }
  
    // Función para convertir la matriz (arreglo 2D) en una cadena: filas separadas por ';' y elementos por ','
    function convertMatrixToString(matrix) {
      return matrix.map(row => row.join(',')).join(';');
    }
  
    // Función para convertir un vector en cadena separada por comas
    function convertVectorToString(vector) {
      return vector.join(',');
    }
  
    // Manejo del envío del formulario
    form.addEventListener('submit', function(e) {
      e.preventDefault();
  
      // Lee los valores de la matriz A
      const matrixInputs = matrixAContainer.querySelectorAll('input');
      const A = [];
      let index = 0;
      for (let i = 0; i < matrixSize; i++) {
        const row = [];
        for (let j = 0; j < matrixSize; j++) {
          row.push(parseFloat(matrixInputs[index].value));
          index++;
        }
        A.push(row);
      }
  
      // Lee los valores del vector b
      const vectorBInputs = vectorBContainer.querySelectorAll('input');
      const b = Array.from(vectorBInputs).map(input => parseFloat(input.value));
  
      // Lee los valores del vector x0
      const vectorX0Inputs = vectorX0Container.querySelectorAll('input');
      const x0 = Array.from(vectorX0Inputs).map(input => parseFloat(input.value));
  
      const tolerancia = parseFloat(document.getElementById('tolerancia').value);
      const max_iter = parseInt(document.getElementById('max_iter').value);
  
      // Construye el payload, incluyendo el campo matrix_size
      const payload = {
        matrix_size: matrixSize,
        A: convertMatrixToString(A),
        b: convertVectorToString(b),
        x0: convertVectorToString(x0),
        tolerancia: tolerancia,
        max_iter: max_iter
      };
  
      console.log("Enviando payload:", payload);  // Para depuración
  
      // Realiza la petición POST usando fetch a localhost
      fetch('http://localhost:5000/calcular_jacobi', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      .then(response => response.json())
      .then(data => {
        if (data.resultado !== undefined) {
          resultContainer.innerHTML = `<div class="card resultado"><span>Resultado = ${data.resultado.join(', ')}</span></div>`;
        } else {
          resultContainer.innerHTML = `<div class="card resultado error"><span>ERROR: ${data.error || 'Error inesperado'}</span></div>`;
        }
      })
      .catch(error => {
        console.error('Error de conexión:', error);
        resultContainer.innerHTML = `<div class="card resultado error"><span>Error de conexión</span></div>`;
      });
    });
  });
  