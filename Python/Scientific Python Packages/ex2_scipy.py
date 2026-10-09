import numpy as np
from scipy.optimize import minimize_scalar
from scipy.integrate import solve_ivp

W, S, CD0, e, AR = 220000.0, 54.0, 0.022, 0.82, 11.0
rho_SL, h0 = 1.225, 6000.0
k = 1.0 / (np.pi * e * AR)

def isa_density(h):
    """ISA density in the troposphere, h in metres."""
    return rho_SL * (1.0 - 2.2558e-5 * h)**4.2561

# Task 1: best glide speed
def drag_over_lift(V, rho):
    """CD / CL in steady flight at speed V and density rho."""
    CL = W / (0.5 * rho * V**2 * S)  # TODO
    CD = CD0 + k * CL**2  # TODO
    return CD / CL  # TODO

result = minimize_scalar(drag_over_lift, bounds=(40.0, 250.0),
                         args=(isa_density(h0),), method="bounded")
print("Optimiser converged:", result.success)

V_best   = result.x
LD       = 1.0 / result.fun
gamma    = np.arctan(result.fun)          # glide angle in radians
CL_best  = np.sqrt(CD0 / k)

print(f"Best glide speed  {V_best:8.2f} m/s")
print(f"L/D at that speed {LD:8.2f}   (closed form {1 / (2 * np.sqrt(CD0 * k)):.2f})")
print(f"Glide angle       {np.degrees(gamma):8.3f} deg")

# Task 2: integrate the glide trajectory
def glide_odes(t, state):
    """state = [x, h]; returns [dx/dt, dh/dt] for a steady best-glide descent."""
    x, h = state
    rho  = isa_density(max(h, 0.0))
    V    = np.sqrt(W / (0.5 * rho * S * CL_best))  # TODO: speed that holds CL_best at this density, from the lift equation
    return [ V * np.cos(gamma),  # TODO: dx/dt
             -V * np.sin(gamma)   # TODO: dh/dt (negative, the aircraft is descending)
           ]

def touchdown(t, state):
    return state[1]            # triggers when altitude reaches zero
touchdown.terminal  = True
touchdown.direction = -1

sol = solve_ivp(glide_odes, (0.0, 3600.0), [0.0, h0],
                events=touchdown, max_step=5.0)

print("Solver message:", sol.message)
glide_range = sol.y_events[0][0][0]
glide_time  = sol.t_events[0][0]
print(f"Glide range {glide_range / 1000:7.1f} km")
print(f"Time aloft  {glide_time / 60:7.1f} min")
print(f"Check: h0 * L/D = {h0 * LD / 1000:.1f} km")

# Task 3: sensitivity to starting altitude
for h_start in [2000.0, 4000.0, 6000.0, 8000.0, 10000.0]:
    s = solve_ivp(glide_odes, (0.0, 3600.0), [0.0, h_start],
                  events=touchdown, max_step=5.0)
    print(f"  h0 = {h_start:6.0f} m  ->  range {s.y_events[0][0][0] / 1000:6.1f} km")