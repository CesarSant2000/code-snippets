import numpy as np
import matplotlib.pyplot as plt

# Datos iniciales
Ca0 = 1000  # mol/m^3
Das = 1.5e-10  # m^2/s
L = 0.5  # m
k = 0.5  # s^-1
v = 0.01  # m/s

# Solicitar número de nodos
#n = int(input('Ingrese el número de nodos: '))  # Número de nodos

# Valores de nodos a graficar
n_values = [10, 50, 100, 200]

# Crear la figura
plt.figure(figsize=(10, 6))

for n in n_values:
    dz = L / (n - 1)
    z = np.linspace(0, L, n)

    # Cálculo de los coeficientes
    a = (2 * Das) / (v * dz)
    b = (2 * k * dz) / v

    # Crear la matriz A
    A = np.zeros((n - 2, n - 2))  # Matriz de coeficientes
    # A[0, 0] = 2 * a + b # Aquí estamos asumiendo que el primer elemento de la matriz es diferente de todos, ademas de que igual
    # se va a sobreescribir en la siguiente iteración por lo que no es necesario, siempre es bueno analizar linea por linea lo que quiero
    # lograr o en su defecto, imaginarte como va a ir quedando

    # for i in range(1, n - 2): # Arriba habiamos definido el primer elemento, pero nos estamos olvidando de todo el resto de la primera fila
    # por lo que hacemos que inicie desde 0 
    #     A[i, i] = 2 * a + b             # Elemento diagonal # Aqui todo lo veo bien
    #     A[i - 1, i] = -(1 + a)          # Elemento superior # recordemos que ahora comienza en 0 por lo que deberia ser i y no i - 1, 
    # agregamos una condicion para no tener un error de indice
    #     A[i, i - 1] = (1 - a)           # Elemento inferior # Esto solo se va a cumplir siempre que i sea mayor a 0 o si no se va a romper
    # por lo que agregamos una condicion para controlar esto, ademas de que al ir desde i = 0 ya no debe ser en la fila i - 1 si no en la i

    for i in range(n - 2):
        A[i, i] = 2 * a + b  # Elemento diagonal
        if i < n - 3:
            A[i, i + 1] = (1 - a)  # Elemento superior
        if i > 0:
            A[i, i - 1] = -(1 + a)  # Elemento inferior

    # Crear el vector R
    R = np.zeros((n - 2, 1))
    R[0, 0] = (1 + a) * Ca0  # Primer valor de concentración

    # Resolver el sistema A * C = R
    C = np.linalg.solve(A, R)

    # Incluir las condiciones de frontera
    C = np.vstack([Ca0, C, 0])  # Conc. inicial Ca0 y final 0
    
    # Graficar el resultado para este número de nodos
    plt.plot(z, C, label=f'n = {n}', linewidth=2)

# Graficar el resultado
# plt.plot(z, C, 'b-', linewidth=2)
plt.xlabel('Longitud (m)')
plt.ylabel('Concentración (mol/m^3)')
plt.title('Perfil de concentración a lo largo de la longitud')
plt.legend() # To know which line is which
plt.grid(True)
plt.show()
