import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

m0, S, CD0, e, AR = 78000.0, 122.4, 0.026, 0.80, 9.4
T_SL, TSFC, V_CAS = 240000.0, 1.65e-5, 155.0
h_cruise, rho_SL, g, R = 10668.0, 1.225, 9.81, 287.05
k = 1.0 / (np.pi * e * AR)
rho_11 = rho_SL * (1.0 - 2.2558e-5 * 11000.0)**4.2561

# Task 1: the standard atmosphere, working on scalars and arrays alike
def isa_density(h):
    h = np.asarray(h, dtype=float)
    troposphere  = rho_SL * (1.0 - 2.2558e-5 * np.minimum(h, 11000.0))**4.2561
    stratosphere = rho_11 * np.exp(-g * (h - 11000.0) / (R * 216.65))
    return np.where(h <= 11000.0, troposphere, stratosphere)

print(isa_density(np.array([0.0, 5000.0, 11000.0, 11001.0])))

# Task 2: equations of motion
def climb_odes(t, state):
    h, x, m = state
    rho = float(isa_density(h))
    V   = V_CAS * np.sqrt(rho_SL / rho)  # true airspeed at this altitude from V_CAS
    W   = m * g
    CL  = min(W / (0.5 * rho * V**2 * S), 1.5)     # clamp to avoid a silly CL at low speed
    CD  = CD0 + CL**2 / (np.pi * e * AR)
    D   = 0.5 * rho * V**2 * S * CD 
    T   = T_SL * (rho / rho_SL)**0.9  # thrust with the density lapse
    sin_gamma = max((T - D) / W, 0.0)              # never descend
    gamma = np.arcsin(min(sin_gamma, 1.0))
    dh_dt = V * np.sin(gamma)
    dx_dt = V * np.cos(gamma)
    dm_dt = -TSFC * T
    return [ dh_dt, dx_dt, dm_dt]

# Task 3: integrate to cruise altitude
def reached_cruise(t, state):
    return state[0] - h_cruise
reached_cruise.terminal  = True
reached_cruise.direction = 1

sol = solve_ivp(climb_odes, (0.0, 3600.0), [0.0, 0.0, m0],
                events=reached_cruise, max_step=10.0)
print(sol.success, sol.message)

t_climb = sol.t[-1]
print(f"Time to climb   {t_climb / 60:8.2f} min")
print(f"Distance        {sol.y[1, -1] / 1000:8.1f} km")
print(f"Fuel burned     {m0 - sol.y[2, -1]:8.0f} kg")
print(f"Mean rate of climb {h_cruise / (t_climb / 60):7.0f} m/min")

# Task 4: trajectory in a DataFrame
df = pd.DataFrame({"t_s": sol.t, "h_m": sol.y[0], "x_m": sol.y[1], "mass_kg": sol.y[2]})
df["rho"] = isa_density(df["h_m"].to_numpy())
df["V_ms"] = V_CAS * np.sqrt(rho_SL / df["rho"].to_numpy())  # true airspeed at each point
df["roc_m_min"] = np.gradient(df["h_m"], df["t_s"]) * 60.0
df["fuel_flow_kg_min"] = np.maximum(-np.gradient(df["mass_kg"], df["t_s"]) * 60.0, 0.0)
df["fuel_burned_kg"] = m0 - df["mass_kg"]

bands = pd.cut(df["h_m"], bins=np.arange(0.0, 12001.0, 2000.0))
print(df.groupby(bands, observed=True)[["roc_m_min", "fuel_flow_kg_min", "V_ms"]].mean().round(1))
df.to_csv("climb_trajectory.csv", index=False)

# Task 5: the figure
fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)

ax = axes[0, 0]
ax.plot(df["t_s"] / 60.0, df["h_m"] / 1000.0, color="tab:blue")
ax.axhline(h_cruise / 1000.0, color="tab:red", linestyle="--", linewidth=1.5, label="Cruise altitude")
ax.set_xlabel("Time (min)")
ax.set_ylabel("Altitude (km)")
ax.grid(True, alpha=0.3)
ax.legend()

ax = axes[0, 1]
ax.plot(df["V_ms"], df["h_m"] / 1000.0, color="tab:green")
ax.set_xlabel("True airspeed (m/s)")
ax.set_ylabel("Altitude (km)")
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(df["h_m"] / 1000.0, df["roc_m_min"], color="tab:orange")
ax.set_xlabel("Altitude (km)")
ax.set_ylabel("Rate of climb (m/min)")
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.plot(df["t_s"] / 60.0, df["fuel_burned_kg"], color="tab:purple")
ax.set_xlabel("Time (min)")
ax.set_ylabel("Cumulative fuel burned (kg)")
ax.grid(True, alpha=0.3)

fig.suptitle("Climb performance, sea level to FL350", fontsize=14)
fig.savefig("climb_performance.pdf", bbox_inches="tight")
plt.show()