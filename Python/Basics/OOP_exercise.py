import math
import numpy as np

class TakeoffDistance:

    def __init__(self, weight, wing_area, cl_max, cd_ground, cd_air, thrust, engine_designation, g=9.81, h_screen=15.24):
        # Constant aircraft and physical data passed to the constructor
        self.weight = weight                    # Aircraft weight (W) in N[cite: 3]
        self.wing_area = wing_area              # Wing area (S) in m^2[cite: 3]
        self.cl_max = cl_max                    # Maximum lift coefficient (C_L,max)[cite: 3]
        self.cd_ground = cd_ground              # Ground roll drag coefficient (CD_ground)[cite: 3]
        self.cd_air = cd_air                    # Airborne drag coefficient (CD_air)[cite: 3]
        self.thrust = thrust                    # Total engine thrust (T) in N[cite: 3]
        self.engine_designation = engine_designation  # String for reporting[cite: 3]
        self.g = g                              # Acceleration due to gravity in m/s^2
        self.h_screen = h_screen                # Screen height in meters[cite: 2]

    def liftoff_speed(self, density):
        # Equation in syllabus
        return 1.2 * np.sqrt((2 * self.weight) / (density * self.wing_area * self.cl_max))

    def mean_acceleration(self, density, mu):
        # Equation in syllabus
        v_l0 = self.liftoff_speed(density)
        v_7 = 0.7 * v_l0
        # Must calculate lift and drag at 70% of liftoff speed to find mean acceleration
        lift = 0.5 * density * v_7**2 * self.wing_area * self.cl_max
        drag = 0.5 * density * v_7**2 * self.wing_area * self.cd_ground
        # Given equation for mean acceleration
        a_bar = (self.g / self.weight) * (self.thrust - drag - mu * (self.weight - lift))
        return a_bar

    def ground_roll(self, density, mu):
        # Equation in syllabus
        v_l0 = self.liftoff_speed(density)
        a_bar = self.mean_acceleration(density, mu)
        return v_l0**2 / (2 * a_bar)

    def airborne_distance(self, density):
        # Equation in syllabus
        v_lo = self.liftoff_speed(density)
        drag_air = 0.5 * density * v_lo**2 * self.wing_area * self.cd_air
        tan_gamma = (self.thrust - drag_air) / (self.weight)
        return self.h_screen / tan_gamma

    def factored_tod(self, density, mu):
        s_a = self.airborne_distance(density)
        s_g = self.ground_roll(density, mu)
        TOD = s_g + s_a
        return 1.15 * TOD

    def performance_report(self, density, mu):
        v_lo = self.liftoff_speed(density)
        s_g = self.ground_roll(density, mu)
        s_a = self.airborne_distance(density)
        tod = s_g + s_a
        tod_factored = self.factored_tod(density, mu)
        
        print(f"=== Takeoff Performance Report ({self.engine_designation}) ===")
        print(f"Air Density (rho): {density} kg/m^3")
        print(f"Friction Coefficient (mu): {mu}")
        print(f"Liftoff Speed (V_LO): {v_lo:.2f} m/s ({v_lo * 1.94384:.1f} knots)")
        print(f"Ground Roll Distance (s_ground): {s_g:.2f} m")
        print(f"Airborne Distance (s_air): {s_a:.2f} m")
        print(f"Total Takeoff Distance (TOD): {tod:.2f} m")
        print(f"Factored TOD (CS-25, 1.15x): {tod_factored:.2f} m")
        print("==================================================")

    def __str__(self):
        return f"TakeoffDistance Model for {self.engine_designation} (Weight: {self.weight} N, Wing Area: {self.wing_area} m^2)"

    def __repr__(self):
        return (f"TakeoffDistance(weight={self.weight}, wing_area={self.wing_area}, "
                f"cl_max={self.cl_max}, cd_ground={self.cd_ground}, cd_air={self.cd_air}, "
                f"thrust={self.thrust}, engine_designation='{self.engine_designation}')")

## Task 1 : Instantiate and verify

A320 = TakeoffDistance(
    weight=2940000,          # W in N[cite: 2]
    wing_area=122.4,         # S in m^2[cite: 2]
    cl_max=2.50,             # CL_max[cite: 2]
    cd_ground=0.05,          # CD_ground[cite: 2]
    cd_air=0.04,             # CD_air[cite: 2]
    thrust=240000,           # T in N[cite: 2]
    engine_designation="Airbus A320-200"
)

A320.performance_report(density = 1.225, mu = 0.02)

## Task 2 : Friction coefficient study (runway surface condition)

runway_conditions = [
    ("Dry concrete", 0.02),
    ("Wet runway", 0.05),
    ("Contaminated (slush)", 0.10)
]

runway_available = 2500
density_isa = 1.225

print("\n=== Task 2: Runway Friction Performance Study ===")
print(f"{'Condition':<25} | {'mu':<5} | {'Factored TOD (m)':<16} | {'Margin (m)':<12} | {'Status'}")
print("-" * 85)

for condition, mu in runway_conditions:
    tod_factored = A320.factored_tod(density_isa, mu)
    margin = runway_available - tod_factored
    if tod_factored > runway_available:
        status = "Insufficient"
    else:
        status = "Sufficient"
    print(f"{condition:<25} | {mu:<5.2f} | {tod_factored:<16.2f} | {margin:<12.2f} | {status}")

## Task 3 : Density altitude study (hot and high conditions)

def isa_density(h):
    rho_0 = 1.225
    T_0 = 288.15
    lapse_rate = 0.0065
    g = 9.80665
    R = 287.05

    T_h = T_0 - lapse_rate * h

    exponent = (g / (R * lapse_rate)) - 1
    rho_h = rho_0 * (T_h / T_0) ** exponent
    return rho_h

altitude = np.arange(0, 1001, 100)
mu_dry = 0.02

print("\n=== Task 3: Density Altitude Study (0 - 1000 m) ===")
print(f"{'Altitude (m)':<15} | {'Density (kg/m^3)':<18} | {'Factored TOD (m)':<16} | {'Status'}")
print("-" * 75)

for h in altitude:
    density_h = isa_density(h)
    tod_factored = A320.factored_tod(density_h, mu_dry)
    if tod_factored > runway_available:
        status = "Insufficient"
    else:
        status = "Sufficient"
    print(f"{h:<15} | {density_h:<18.4f} | {tod_factored:<16.2f} | {status}")