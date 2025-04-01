import numpy as np

def gauss_seidel(A, b, x0, tolerancia=1e-6, max_iter=100):
    A, b = reordenar_matriz(A, b)

    if not es_diagonal_dominante(A):
        raise ValueError("La matriz no es diagonal dominante. El método de Gauss-Seidel puede no converger.")

    n = len(b)
    x = x0.copy()
    x_new = np.zeros_like(x0)
    
    for k in range(max_iter):
        for i in range(n):
            s1 = sum(A[i, j] * x[j] for j in range(i))
            s2 = sum(A[i, j] * x_new[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        
        error = np.linalg.norm(x_new - x, ord=np.inf)
        
        if error < tolerancia:
            return x_new
        
        x = x_new.copy()
    
    return None

def es_diagonal_dominante(A):
    D = np.abs(A.diagonal())  
    S = np.sum(np.abs(A), axis=1) - D 
    return np.all(D >= S)

def reordenar_matriz(A, b):
    n = len(A)
    for i in range(n):
        max_index = np.argmax(np.abs(A[i:, i])) + i
        if i != max_index:
            A[[i, max_index]] = A[[max_index, i]]
            b[[i, max_index]] = b[[max_index, i]]
    return A, b