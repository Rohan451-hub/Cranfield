import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

L     = 1.0      # domain length (m)
alpha = 0.01     # thermal diffusivity (m^2/s)
N     = 50       # interior grid points
dx    = L / (N + 1)
dt    = 0.02     # time step (s); BTCS is unconditionally stable
T_end = 4.0      # total simulation time (s)
x     = np.linspace(0, L, N + 2)[1:-1]   # interior coordinates

## Task 1

r         = alpha * dt / dx**2
diag_main = (1 + 2 * r) * np.ones(N)
diag_sub  = -r * np.ones(N - 1)
diag_sup  = -r * np.ones(N - 1)
A_btcs    = sp.diags([diag_sub, diag_main, diag_sup], [-1, 0, 1], format='csr')

x0      = 0.3    # hot-spot location (m)
sigma_g = 0.06   # Gaussian width (m)
T       = np.exp(-0.5 * ((x - x0) / sigma_g)**2)

n_steps = int(T_end / dt)
snapshots = [T.copy()]

# Loop : A_btcs * T_{n+1} = T_n
for _ in range(n_steps):
    T = spsolve(A_btcs, T)
    snapshots.append(T.copy())

# snapshots U matrix (N, n_snapshots + 1)
U = np.array(snapshots).T

print("Shape of the snapshot matrix U :", U.shape)

# First column should be the initial condition (Gaussian)
print("First column is valid :", np.allclose(U[:, 0], np.exp(-0.5 * ((x - x0) / sigma_g)**2)))

# Last column should be close to zero (steady state)
print("Maximum value at the end (close to 0) :", np.max(np.abs(U[:, -1])))

## Task 2

Phi, sigma, VT = np.linalg.svd(U, full_matrices=False)

total_energy = np.sum(sigma**2)
energy       = sigma**2 / total_energy
cumulative   = np.cumsum(energy)

print(f"{'Mode':<6} | {'Singular Value':<16} | {'Energy Fraction':<16} | {'Cumulative Energy':<18}")
print("-" * 65)
for i in range(min(10, len(sigma))):
    print(f"{i+1:<6} | {sigma[i]:<16.6e} | {energy[i]:<16.6e} | {cumulative[i]*100:<17.4f}%")

k = np.argmax(cumulative >= 0.999) + 1

print("-" * 65)
print(f"Smallest k for cumulative energy > 99.9%: k = {k}")

## Task 3

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left Panel

mode_indices = np.arange(1, len(sigma) + 1)
ax1.semilogy(mode_indices, sigma, 'o-', markersize=4)
ax1.set_xlabel('Mode index $i$')
ax1.set_ylabel('Singular value $\sigma_i$')
ax1.set_title('Singular Value Spectrum')
ax1.grid(True, which="both", ls="--")

# Right Panel

for i in range(4):
    ax2.plot(x, Phi[:, i], label=f'Mode {i+1}')

ax2.set_xlabel('Position $x$ (m)')
ax2.set_ylabel('Mode amplitude')
ax2.set_title('First Four POD Modes')
ax2.legend()
ax2.grid(True)

plt.tight_layout()

# Save the figure

plt.savefig('pod_spectrum.pdf')
plt.show()

## Task 4

k_values = [1, 3, 5, 10]
errors = []

# Compute the total Frobenius norm of U for relative error calculation
norm_U = np.linalg.norm(U, 'fro')

for k in k_values:
    # Reconstruct the full matrix U_k using k modes
    U_k = Phi[:, :k] @ np.diag(sigma[:k]) @ VT[:k, :]
    
    # Compute relative error (Frobenius norm)
    error_k = np.linalg.norm(U - U_k, 'fro') / norm_U
    errors.append(error_k)
    print(f"k = {k:2d} | Relative error: {error_k:.6e}")

# 2. Plot 1: Relative error vs k on a semilogy axis
plt.figure(figsize=(8, 5))
plt.semilogy(k_values, errors, 'o-', linewidth=2, label='Reconstruction error')

# Add horizontal dashed annotation lines for 1%, 0.1%, and 0.01% error levels
plt.axhline(y=0.01, color='r', linestyle='--', alpha=0.7, label='1% threshold')
plt.axhline(y=0.001, color='g', linestyle='--', alpha=0.7, label='0.1% threshold')
plt.axhline(y=0.0001, color='b', linestyle='--', alpha=0.7, label='0.01% threshold')

plt.xlabel('Number of modes $k$')
plt.ylabel('Relative error (Frobenius norm)')
plt.title('Relative Reconstruction Error vs $k$')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.tight_layout()
plt.show()

# 3. Plot 2: Field comparison at a single time snapshot near the middle of simulation
mid_index = U.shape[1] // 2  # Snapshot index near the middle
t_mid = mid_index * dt

plt.figure(figsize=(8, 5))

# Original field (thick black line)
plt.plot(x, U[:, mid_index], 'k-', linewidth=3, label=f'Original (t = {t_mid:.2f}s)')

# Reconstructions for k = 1, 3, and 5 (coloured dashed lines)
colors = ['red', 'green', 'blue']
for k, color in zip([1, 3, 5], colors):
    U_k = Phi[:, :k] @ np.diag(sigma[:k]) @ VT[:k, :]
    plt.plot(x, U_k[:, mid_index], linestyle='--', color=color, linewidth=2, label=f'Reconstruction (k={k})')

plt.xlabel('Position $x$ (m)')
plt.ylabel('Temperature $T$')
plt.title(f'Temperature Field Comparison at $t = {t_mid:.2f}$ s')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

## Task 5

# 1. Solve the heat equation for the new initial condition (hot spot shifted to x0 = 0.6)
x0_new = 0.6
T_new = np.exp(-0.5 * ((x - x0_new) / sigma_g)**2)

snapshots_new = [T_new.copy()]
for _ in range(n_steps):
    T_new = spsolve(A_btcs, T_new)
    snapshots_new.append(T_new.copy())

# True snapshot matrix for the new simulation
U_new = np.array(snapshots_new).T

# 2. Extract modal coefficients by projecting onto the existing POD basis using k = 5
k_task5 = 5
Phi_k = Phi[:, :k_task5]

# Modal coefficients for each time step: shape (k, n_snapshots + 1)
coefficients = Phi_k.T @ U_new

# Reconstruct the field from modal coefficients
U_reconstructed = Phi_k @ coefficients

# 3. Compare true and reconstructed fields at early, middle, and late time levels
target_times = [0.2, 2.0, 3.8]
indices = [int(round(t / dt)) for t in target_times]

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

for ax, idx, t in zip(axes, indices, target_times):
    true_field = U_new[:, idx]
    recon_field = U_reconstructed[:, idx]
    
    # Compute relative L2 error at time t
    l2_error = np.linalg.norm(true_field - recon_field) / np.linalg.norm(true_field)
    
    # Plot true vs reconstructed fields
    ax.plot(x, true_field, 'k-', linewidth=2.5, label='True Field')
    ax.plot(x, recon_field, 'r--', linewidth=2, label=f'Reconstructed (k={k_task5})')
    
    ax.set_xlabel('Position $x$ (m)')
    ax.set_title(f'$t = {t:.1f}$ s\nRelative $L_2$ Error: {l2_error:.4%}')
    ax.grid(True)
    ax.legend()

axes[0].set_ylabel('Temperature $T$')
plt.suptitle('Prediction of an Unseen Field ($x_0 = 0.6$) via POD Projection', fontsize=14)
plt.tight_layout()
plt.show()