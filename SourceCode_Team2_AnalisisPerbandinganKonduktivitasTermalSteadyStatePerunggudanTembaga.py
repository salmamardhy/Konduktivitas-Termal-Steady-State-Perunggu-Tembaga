import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

# Inputs
q = 1830000  # Heat generation, W/m3
xlength = 1  # unit say m, length
yheight = 1  # unit say m, height
nx = 40  # no of segments of xlength, e.g., 4, 30
deltax = xlength / nx  # unit say m deltax = deltay
T1 = 200  # Temperature in deg.C (typ)
T2 = 200
T3 = 200
T4 = 200
D_1 = []
D_2 = []
label_name = ["Copper", "Bronze"]

for iter in range(2):
    k = [398, 120]  # Thermal Conductivity, W/(m K) ()
    k = k[iter]

    # Solution
    m = int((xlength / deltax) - 1)  # no. of interior points in any row
    n = int((yheight / deltax) - 1)  # no. of interior points in any column
    r = n * m  # Total no. of interior points
    f = (deltax**2) * (q / k)  # factor

    # Creating a matrix
    a = np.zeros((r, r))
    for i in range(r):
        for j in range(r):
            if i == j:
                a[i, j] = -4
            elif (i == j + 1) and (i % n != 0):
                a[i, j] = 1
            elif (i == j - 1) and (j % n != 0):
                a[i, j] = 1
            elif i == j + n:
                a[i, j] = 1
            elif i == j - n:
                a[i, j] = 1

    # Creating b vector
    d = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            if (i == 0) and (j == 0):
                d[i, j] = -(T1 + T4)
            elif (j == 0) and (i > 0) and (i < m - 1):
                d[i, j] = -T1
            elif (j == 0) and (i == m - 1):
                d[i, j] = -(T1 + T2)
            elif (i == m - 1) and (j > 0) and (j < n - 1):
                d[i, j] = -T2
            elif (i == m - 1) and (j == n - 1):
                d[i, j] = -(T2 + T3)
            elif (j == n - 1) and (i > 0) and (i < m - 1):
                d[i, j] = -T3
            elif (i == 0) and (j == n - 1):
                d[i, j] = -(T3 + T4)
            elif (i == 0) and (j > 0) and (j < n - 1):
                d[i, j] = -T4
    

    dl = -f * np.ones((m, n))
    d3 = d + dl

    matrix = np.reshape(d3, (1, m * n))

    # Above to match ppt
    b2 = matrix.T

    # Solve the linear system
    x = np.linalg.solve(a, b2)

    # Creating T matrix
    T = np.zeros((m + 2, n + 2))
    k = 0

    for i in range(1, m+1):
        for j in range(1, n+1):
            T[i, j] = x[k]
            k += 1
    
    T2D = T[1:m + 1, 1:n + 1].T
    
    for i in range(2):
        T1D = np.zeros(m)
        for j in range(m):
            T1D[j] = T[j + 1, int(n/2) + 1]  # Get temperature at the middle point of y axis

    D_2.append(T2D)
    D_1.append(T1D)

# Plot contour graphs for D_2
fig = plt.figure(figsize=(10, 10))
gs = gridspec.GridSpec(2, 2, height_ratios=[1.6, 1.2])
gs.update(wspace=0.5, hspace=0.5)

for i in range(2):
    # Plot contour graphs for D_2
    vmin = min(np.min(D_2[0]), np.min(D_2[1]))
    vmax = max(np.max(D_2[0]), np.max(D_2[1]))

    ax = fig.add_subplot(gs[i])
    x = D_2[i]
    extent = [0, xlength, 0, yheight]
    im = ax.imshow(x, cmap=plt.cm.jet, origin='upper', vmin=vmin, vmax=vmax, extent=extent, aspect='auto')
    ax.set_title(f'Temperature Profile 2D for {label_name[i]}\nT1 = {T1} deg.C', fontsize=11)
    ax.set_xlabel(f'x\nT3 = {T3} deg.C')
    ax.set_ylabel(f'y\nT4 = {T4} deg.C')
    cbar = fig.colorbar(im, ax=ax, pad=0.07)
    cbar.ax.yaxis.set_label_position('left')
    cbar.ax.set_ylabel(f'T2 = {T2} deg.C', labelpad=3)


    # Plot 1D graphs for D_1
    vmin = min(np.min(D_1[0]), np.min(D_1[1]))
    vmax = max(np.max(D_1[0]), np.max(D_1[1]))

    ax = fig.add_subplot(gs[i + 2])
    x = D_1[i]
    ax.plot(x)
    ax.set_title(f'Temperature Profile 1D for {label_name[i]}', fontsize=11)
    ax.set_xlabel('x (m)', labelpad=10)
    ax.set_ylabel('Temperature (deg.C)', labelpad=10)
    ax.set_ylim(vmin+15, vmax+15)

# Find the maximum data in D_1
max_C, min_C = np.max(D_1[0]), np.min(D_1[0])
max_B, min_B = np.max(D_1[1]), np.min(D_1[1])

print(f"Temperatur minimum dan maksimum pada material {label_name[0]} = {min_C:.3f} deg.C dan {max_C:.3f} deg.C")
print(f"Temperatur minimum dan maksimum pada material {label_name[1]} = {min_B:.3f} deg.C dan {max_B:.3f} deg.C")

# Adjust aspect ratio and spacing
fig.subplots_adjust(hspace=0.8)
title = fig.suptitle(f'Temperature Profiles Material', fontsize=15, y=0.98)
plt.show()