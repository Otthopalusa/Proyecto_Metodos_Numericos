from microservicios.newton_service import resolver_newton_raphson
from microservicios.punto_fijo_service import resolver_punto_fijo
from microservicios.secante_service import resolver_secante
from tabulate import tabulate

#=========================================================================================================
def mostrar_menu():
    """
    Muestra el menú principal de la aplicación.
    """
    print("\n===== CALCULADORA DE MÉTODOS NUMÉRICOS =====")
    print("1. Método de Newton-Raphson")
    print("2. Método de Punto Fijo")
    print("3. Método de la Secante")
    print("4. Salir")
    return input("Seleccione una opción (1-4): ")

#=========================================================================================================
def ejecutar_newton_raphson():
    """
    Solicita los datos para el método de Newton-Raphson y muestra los resultados en una tabla.
    """
    print("\n--- MÉTODO DE NEWTON-RAPHSON ---")
    ecuacion = input("Ingrese la ecuación (ejemplo: x**2 - 4): ")
    x0 = float(input("Ingrese el valor inicial (x0): "))
    tolerancia = float(input("Ingrese la tolerancia (por defecto 1e-6): ") or "1e-6")
    max_iter = int(input("Ingrese el número máximo de iteraciones (por defecto 100): ") or "100")
    
    resultado = resolver_newton_raphson(ecuacion, x0, tolerancia, max_iter)
    
    if 'error' in resultado:
        print(f"\nError: {resultado['error']}")
    else:
        print(f"\nRaíz encontrada: {resultado['raiz']}")
        print(f"Mensaje: {resultado['mensaje']}")
        
        # Crear tabla de iteraciones
        tabla_datos = []
        for i, (iteracion, error) in enumerate(resultado['errores']):
            x_n = x0 if i == 0 else resultado['valores_x'][i-1]
            f_x = resultado['valores_fx'][i]
            f_prima_x = resultado['valores_fpx'][i]
            x_sig = resultado['valores_x'][i]
            
            tabla_datos.append([
                iteracion,
                f"{x_n:.6f}",
                f"{f_x:.6f}",
                f"{f_prima_x:.6f}",
                f"{x_sig:.6f}",
                f"{error:.6f}%"
            ])
        
        headers = ["Iteración", "x_n", "f(x_n)", "f'(x_n)", "x_{n+1}", "Error (%)"]
        print("\nTabla de iteraciones:")
        print(tabulate(tabla_datos, headers=headers, tablefmt="grid"))

#=========================================================================================================
def ejecutar_punto_fijo():
    """
    Solicita los datos para el método de Punto Fijo y muestra los resultados en una tabla.
    """
    print("\n--- MÉTODO DE PUNTO FIJO ---")
    ecuacion = input("Ingrese la ecuación (ejemplo: x**2 - 4): ")
    x0 = float(input("Ingrese el valor inicial (x0): "))
    tolerancia = float(input("Ingrese la tolerancia (por defecto 1e-4): ") or "1e-4")
    max_iter = int(input("Ingrese el número máximo de iteraciones (por defecto 100): ") or "100")
    
    resultado = resolver_punto_fijo(ecuacion, x0, max_iter, tolerancia)
    
    if 'error' in resultado:
        print(f"\nError: {resultado['error']}")
    else:
        raiz = resultado['raiz']
        if raiz['imag'] == 0:
            print(f"\nRaíz encontrada: {raiz['real']}")
        else:
            print(f"\nRaíz encontrada: {raiz['real']} + {raiz['imag']}i")
        
        print(f"Mensaje: {resultado['mensaje']}")
        
        # Crear tabla de iteraciones
        tabla_datos = []
        for i, (iteracion, error) in enumerate(resultado['errores']):
            x_n = resultado['aproximaciones'][i]
            g_x = resultado['aproximaciones'][i+1]
            
            if isinstance(x_n, complex):
                tabla_datos.append([
                    iteracion,
                    f"{x_n.real:.6f} + {x_n.imag:.6f}i",
                    f"{g_x.real:.6f} + {g_x.imag:.6f}i",
                    f"{error:.6f}%"
                ])
            else:
                tabla_datos.append([
                    iteracion,
                    f"{x_n:.6f}",
                    f"{g_x:.6f}",
                    f"{error:.6f}%"
                ])
        
        headers = ["Iteración", "x_n", "g(x_n)", "Error (%)"]
        print("\nTabla de iteraciones:")
        print(tabulate(tabla_datos, headers=headers, tablefmt="grid"))

#=========================================================================================================
def ejecutar_secante():
    """
    Solicita los datos para el método de la Secante y muestra los resultados en una tabla.
    """
    print("\n--- MÉTODO DE LA SECANTE ---")
    ecuacion = input("Ingrese la ecuación (ejemplo: x**2 - 4): ")
    x0 = float(input("Ingrese el primer valor inicial (x0): "))
    x1 = float(input("Ingrese el segundo valor inicial (x1): "))
    tolerancia = float(input("Ingrese la tolerancia (por defecto 1e-5): ") or "1e-5")
    max_iter = int(input("Ingrese el número máximo de iteraciones (por defecto 100): ") or "100")
    
    resultado = resolver_secante(ecuacion, x0, x1, tolerancia, max_iter)
    
    if 'error' in resultado:
        print(f"\nError: {resultado['error']}")
    else:
        print(f"\nRaíz encontrada: {resultado['raiz']}")
        print(f"Mensaje: {resultado['mensaje']}")
        
        # Crear tabla de iteraciones
        tabla_datos = []
        valores_x = resultado['valores_x']
        valores_fx = resultado['valores_fx']
        
        # Agregar los valores iniciales
        tabla_datos.append([
            0,
            f"{x0:.6f}",
            f"{valores_fx[0]:.6f}",
            "-",
            "-"
        ])
        
        tabla_datos.append([
            1,
            f"{x1:.6f}",
            f"{valores_fx[1]:.6f}",
            "-",
            "-"
        ])
        
        for i, (iteracion, error) in enumerate(resultado['errores']):
            if i+2 < len(valores_x):
                x_i = valores_x[i+1]
                x_i1 = valores_x[i+2]
                f_xi = valores_fx[i+1]
                f_xi1 = valores_fx[i+2]
                
                tabla_datos.append([
                    iteracion+1,
                    f"{x_i1:.6f}",
                    f"{f_xi1:.6f}",
                    f"{(f_xi1-f_xi)/(x_i1-x_i):.6f}",
                    f"{error:.6f}%"
                ])
        
        headers = ["Iteración", "x_n", "f(x_n)", "Secante", "Error (%)"]
        print("\nTabla de iteraciones:")
        print(tabulate(tabla_datos, headers=headers, tablefmt="grid"))

#=========================================================================================================
def main():
    """
    Función principal del programa.
    """
    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            ejecutar_newton_raphson()
        elif opcion == '2':
            ejecutar_punto_fijo()
        elif opcion == '3':
            ejecutar_secante()
        elif opcion == '4':
            print("\n¡Gracias por usar la calculadora de métodos numéricos!")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione una opción del 1 al 4.")

if __name__ == "__main__":
    main()