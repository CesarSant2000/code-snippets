import numpy as np
import matplotlib.pyplot as plt

# Datos iniciales
Ca0 = 1000  # mol/m^3
Das = 1.5e-10  # m^2/s
L = 0.5  # m
k = 0.5  # s^-1
v = 0.01  # m/s

# Solicitar número de nodos
n = int(input('Ingrese el número de nodos: '))  # Número de nodos
dz = L / (n - 1)
z = np.linspace(0, L, n)

# Cálculo de los coeficientes
a = (2 * Das) / (v * dz)
b = (2 * k * dz) / v

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

# Graficar el resultado
plt.plot(z, C, 'b-', linewidth=2)
plt.xlabel('Longitud (m)')
plt.ylabel('Concentración (mol/m^3)')
plt.title('Perfil de concentración a lo largo de la longitud')
plt.grid(True)
plt.show()

# The objective is to form this system of equations
# Matrix form of the system:
#
#   CA_2   CA_3   CA_4   CA_5   CA_6   CA_7   CA_8   CA_9
#
# [ 2a+b   1-a     0     0     0     0     0     0     0 ]   [CA_2]     [ (1+a) * CA_1 ]
# [-(1+a)  2a+b   1-a    0     0     0     0     0     0 ]   [CA_3]     [      0       ]
# [  0    -(1+a)  2a+b  1-a    0     0     0     0     0 ]   [CA_4]     [      0       ]
# [  0      0    -(1+a) 2a+b  1-a    0     0     0     0 ] * [CA_5]  =  [      0       ]
# [  0      0     0    -(1+a) 2a+b  1-a    0     0     0 ]   [CA_6]     [      0       ]
# [  0      0     0     0    -(1+a) 2a+b  1-a    0     0 ]   [CA_7]     [      0       ]
# [  0      0     0     0     0    -(1+a) 2a+b  1-a     0 ]  [CA_8]     [      0       ]
# [  0      0     0     0     0     0    -(1+a) 2a+b   1-a ] [CA_9]     [      0       ]
# [  0      0     0     0     0     0     0    -(1+a)  2a+b] [CA_1]     [      0       ]
#
# This is expressed in matrix form as:
#     K * CA = R
#
# To solve for CA:
#     CA = inv(K) * R
