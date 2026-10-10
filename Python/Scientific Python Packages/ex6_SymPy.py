import sympy as sp
import numpy as np

# Define symbols, including Mach number M and incompressible lift coefficient CL_inc
rho, V, S, CL_inc, W, M = sp.symbols("rho V S C_L_inc W M", positive=True)

# Prandtl-Glauert correction for compressible lift coefficient
CL = CL_inc / sp.sqrt(1 - M**2)

# Lift equation and solving for level flight speed (stall speed)
L = sp.Rational(1, 2) * rho * V**2 * S * CL
V_level = sp.solve(sp.Eq(L, W), V)[0]
print("Level flight speed with Prandtl-Glauert:", sp.simplify(V_level))

# Differentiate speed with respect to Mach number M
dV_dM = sp.diff(V_level, M)
print("dV/dM:", sp.simplify(dV_dM))

# Create numerical functions using lambdify
# Parameters order: rho, S, CL_inc, W, M
V_func = sp.lambdify((rho, S, CL_inc, W, M), V_level, modules="numpy")
dV_dM_func = sp.lambdify((rho, S, CL_inc, W, M), dV_dM, modules="numpy")

# Example input values
rho_val = 1.225
S_val = 122.4
CL_inc_val = 1.5
W_val = 78000 * 9.81

# Evaluate at M = 0.75 and M = 0.85
for m_val in [0.75, 0.85]:
    v_val = V_func(rho_val, S_val, CL_inc_val, W_val, m_val)
    sens_val = dV_dM_func(rho_val, S_val, CL_inc_val, W_val, m_val)
    print(f"\nAt Mach = {m_val}:")
    print(f"  Stall Speed: {v_val:.2f} m/s")
    print(f"  Sensitivity (dV/dM): {sens_val:.2f}")