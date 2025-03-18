import sympy as sp

def punto_fijo(ecuacion, g_x, x0, tolerancia=1e-5, max_iter=100):
    x = sp.symbols('x')
    f = sp.sympify(ecuacion) 
    g = sp.sympify(g_x)

    iteraciones = []
    error = float('inf')
    iter_count = 0

    while error > tolerancia and iter_count < max_iter:
        x1 = g.subs(x, x0).evalf()
        error = abs(x1 - x0)

        iteraciones.append({
            'iteracion': iter_count + 1,
            'x0': x0,
            'x1': x1,
            'error': error
        })

        if error < tolerancia:
            break

        x0 = x1
        iter_count += 1

    return {
        'raiz': x0,
        'iteraciones': iteraciones,
        'convergencia': error < tolerancia
    }
