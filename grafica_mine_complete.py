import numpy as np
import matplotlib.pyplot as plt

# Datos iniciales
Ca0 = 1000  # mol/m^3
Das = 1.5e-10  # m^2/s
L = 0.5  # m
k = 0.5  # s^-1
v = 0.01  # m/s

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
    for i in range(n - 2):
        A[i, i] = 2 * a + b  # Elemento diagonal
        if i > 0:
            A[i, i - 1] = -(1 + a)  # Elemento inferior
        if i < n - 3:
            A[i, i + 1] = (1 - a)  # Elemento superior

    # Crear el vector R
    R = np.zeros((n - 2, 1))
    R[0, 0] = (1 + a) * Ca0  # Primer valor de concentración

    # Resolver el sistema A * C = R
    C = np.linalg.solve(A, R)

    # Incluir las condiciones de frontera
    C = np.vstack([Ca0, C, 0])  # Conc. inicial Ca0 y final 0

    # Graficar el resultado para este número de nodos
    plt.plot(z, C, label=f'n = {n}', linewidth=2)

# Configurar la gráfica
plt.xlabel('Longitud (m)')
plt.ylabel('Concentración (mol/m^3)')
plt.title('Perfil de concentración a lo largo de la longitud para diferentes nodos')
plt.legend()
plt.grid(True)
plt.show()