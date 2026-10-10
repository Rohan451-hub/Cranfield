## Classes and instances

class Airfoil:
    def __init__(self, designation, chord, thickness_ratio, camber):
        self.designation     = designation
        self.chord           = chord           # metres
        self.thickness_ratio = thickness_ratio # t/c, e.g. 0.12 for 12%
        self.camber          = camber          # max camber as fraction of chord

naca2412 = Airfoil(
    designation     = "NACA 2412",
    chord           = 1.5,
    thickness_ratio = 0.12,
    camber          = 0.02
)

naca0009 = Airfoil(
    designation     = "NACA 00092",
    chord           = 1.2,
    thickness_ratio = 0.09,
    camber          = 0.0
)

print(naca2412.designation)      # NACA 2412
print(naca2412.thickness_ratio)  # 0.12
print(naca0009.designation)      # NACA 0009
print(naca0009.thickness_ratio)  # 0.09

class Mesh:
    """This class creates a mesh and converts it to ANSYS Fluent"""
    # ... rest of class implementation

## Methods

class Airfoil:
    def __init__(self, designation, chord, thickness_ratio, camber):
        self.designation     = designation
        self.chord           = chord
        self.thickness_ratio = thickness_ratio
        self.camber          = camber

    def max_thickness(self):
        """Returns the maximum thickness of the airfoil in metres."""
        return self.thickness_ratio * self.chord

    def is_symmetric(self):
        """Returns True if the airfoil has zero camber."""
        return self.camber == 0.0

    def summary(self):
        """Prints a formatted summary of the airfoil geometry."""
        symmetric = "symmetric" if self.is_symmetric() else "cambered"
        print(f"Airfoil:           {self.designation}")
        print(f"Chord:             {self.chord:.3f} m")
        print(f"Thickness ratio:   {self.thickness_ratio:.2%}")
        print(f"Max thickness:     {self.max_thickness():.4f} m")
        print(f"Type:              {symmetric}")

naca2412 = Airfoil("NACA 2412", chord=1.5, thickness_ratio=0.12, camber=0.02)

print(naca2412.max_thickness())  # 0.18
print(naca2412.is_symmetric())   # False

naca2412.summary()
# Airfoil:           NACA 2412
# Chord:             1.500 m
# Thickness ratio:   12.00%
# Max thickness:     0.1800 m
# Type:              cambered

import math

class Airfoil:
    def __init__(self, designation, chord, thickness_ratio, camber):
        self.designation     = designation
        self.chord           = chord
        self.thickness_ratio = thickness_ratio
        self.camber          = camber

    def lift_coefficient_thin_aerofoil(self, alpha_deg):
        """
        Estimates CL using thin aerofoil theory.
        alpha_deg: angle of attack in degrees
        """
        alpha_rad = math.radians(alpha_deg)
        camber_contribution = 2 * math.pi * self.camber
        return 2 * math.pi * alpha_rad + camber_contribution

naca2412 = Airfoil("NACA 2412", chord=1.5, thickness_ratio=0.12, camber=0.02)

for alpha in [0, 2, 4, 6, 8]:
    cl = naca2412.lift_coefficient_thin_aerofoil(alpha)
    print(f"alpha = {alpha:2d} deg  ->  CL = {cl:.4f}")

## Encapsulation and data integrity

class Airfoil:
    def __init__(self, designation, chord, thickness_ratio, camber):
        self.designation      = designation
        self._chord           = chord
        self._thickness_ratio = thickness_ratio
        self._camber          = camber

    @property
    def chord(self):
        """Chord length in metres."""
        return self._chord

    @chord.setter
    def chord(self, value):
        if value <= 0:
            raise ValueError(f"Chord must be positive, got {value}")
        self._chord = value

    @property
    def thickness_ratio(self):
        """Maximum thickness as a fraction of chord (e.g. 0.12 for 12%)."""
        return self._thickness_ratio

    @thickness_ratio.setter
    def thickness_ratio(self, value):
        if not (0 < value < 1):
            raise ValueError(f"Thickness ratio must be between 0 and 1, got {value}")
        self._thickness_ratio = value

    @property
    def camber(self):
        """Maximum camber as a fraction of chord."""
        return self._camber

    @camber.setter
    def camber(self, value):
        if value < 0:
            raise ValueError(f"Camber cannot be negative, got {value}")
        self._camber = value

    naca2412 = Airfoil("NACA 2412", chord=1.5, thickness_ratio=0.12, camber=0.02)

print(naca2412.chord)   # 1.5

naca2412.chord = 2.0    # calls the setter, validation passes
print(naca2412.chord)   # 2.0

naca2412.chord = -1.0   # calls the setter, raises ValueError
# ValueError: Chord must be positive, got -1.0
def __init__(self, designation, chord, thickness_ratio, camber):
        self.designation  = designation
        self.chord           = chord           # calls the setter
        self.thickness_ratio = thickness_ratio # calls the setter
        self.camber          = camber          # calls the setter

## Inheritance

class AerodynamicSurface:
    """Base class representing any aerodynamic surface."""

    def __init__(self, span, chord, sweep_deg):
        self.span      = span        # metres
        self.chord     = chord       # metres
        self.sweep_deg = sweep_deg   # leading edge sweep angle

    def planform_area(self):
        return self.span * self.chord

    def aspect_ratio(self):
        return self.span**2 / self.planform_area()

    def describe(self):
        print(f"Span:          {self.span:.2f} m")
        print(f"Chord:         {self.chord:.2f} m")
        print(f"Planform area: {self.planform_area():.2f} m²")
        print(f"Aspect ratio:  {self.aspect_ratio():.2f}")

class Wing(AerodynamicSurface):
    """Represents a wing, extending AerodynamicSurface with wing-specific attributes."""

    def __init__(self, span, root_chord, tip_chord, sweep_deg, airfoil_designation):
        mean_chord = (root_chord + tip_chord) / 2
        super().__init__(span, mean_chord, sweep_deg)

        self.root_chord           = root_chord
        self.tip_chord            = tip_chord
        self.airfoil_designation  = airfoil_designation

    def taper_ratio(self):
        return self.tip_chord / self.root_chord

    def describe(self):
        super().describe()  # call the parent's describe() first
        print(f"Root chord:    {self.root_chord:.2f} m")
        print(f"Tip chord:     {self.tip_chord:.2f} m")
        print(f"Taper ratio:   {self.taper_ratio():.3f}")
        print(f"Airfoil:       {self.airfoil_designation}")

main_wing = Wing(
    span                  = 35.0,
    root_chord            = 6.0,
    tip_chord             = 3.0,
    sweep_deg             = 28.0,
    airfoil_designation   = "NACA 2412"
)

print(main_wing.aspect_ratio())   # inherited from AerodynamicSurface
print(main_wing.taper_ratio())    # defined in Wing

main_wing.describe()
# Span:          35.00 m
# Chord:         4.50 m
# Planform area: 157.50 m²
# Aspect ratio:  7.78
# Root chord:    6.00 m
# Tip chord:     3.00 m
# Taper ratio:   0.500
# Airfoil:       NACA 2412

## Composition over inheritance

class Engine:
    def __init__(self, designation, thrust_kN, bypass_ratio):
        self.designation  = designation
        self.thrust_kN    = thrust_kN
        self.bypass_ratio = bypass_ratio

    def describe(self):
        print(f"Engine:        {self.designation}")
        print(f"Thrust:        {self.thrust_kN:.1f} kN")
        print(f"Bypass ratio:  {self.bypass_ratio:.1f}")


class Fuselage:
    def __init__(self, length, diameter):
        self.length   = length    # metres
        self.diameter = diameter  # metres

    def fineness_ratio(self):
        return self.length / self.diameter

    def describe(self):
        print(f"Fuselage:      {self.length:.1f} m × {self.diameter:.1f} m")
        print(f"Fineness ratio:{self.fineness_ratio():.2f}")


class Aircraft:
    def __init__(self, name, wing, fuselage, engines):
        self.name     = name
        self.wing     = wing        # a Wing instance
        self.fuselage = fuselage    # a Fuselage instance
        self.engines  = engines     # a list of Engine instances

    def total_thrust_kN(self):
        return sum(engine.thrust_kN for engine in self.engines)

    def thrust_to_weight(self, mass_kg):
        weight_kN = mass_kg * 9.81 / 1000
        return self.total_thrust_kN() / weight_kN

    def describe(self):
        print(f"\n=== {self.name} ===")
        print("\n-- Wing --")
        self.wing.describe()
        print("\n-- Fuselage --")
        self.fuselage.describe()
        print("\n-- Engines --")
        for i, engine in enumerate(self.engines, start=1):
            print(f"  Engine {i}:")
            engine.describe()
        print(f"\nTotal thrust:  {self.total_thrust_kN():.1f} kN")

wing = Wing(
    span                = 35.0,
    root_chord          = 6.0,
    tip_chord           = 3.0,
    sweep_deg           = 28.0,
    airfoil_designation = "NACA 2412"
)

fuselage = Fuselage(length=45.0, diameter=4.2)

engines = [
    Engine("CFM56-7B", thrust_kN=120.0, bypass_ratio=5.1),
    Engine("CFM56-7B", thrust_kN=120.0, bypass_ratio=5.1),
]

airliner = Aircraft("Generic Narrowbody", wing, fuselage, engines)
airliner.describe()

## Special (dunder) methods

class Airfoil:
    def __init__(self, designation, chord, thickness_ratio, camber):
        self.designation     = designation
        self.chord           = chord
        self.thickness_ratio = thickness_ratio
        self.camber          = camber

    def __repr__(self):
        return (f"Airfoil(designation={self.designation!r}, "
                f"chord={self.chord}, "
                f"thickness_ratio={self.thickness_ratio}, "
                f"camber={self.camber})")

    def __str__(self):
        return (f"{self.designation} | "
                f"c = {self.chord:.2f} m | "
                f"t/c = {self.thickness_ratio:.1%} | "
                f"camber = {self.camber:.1%}")

naca2412 = Airfoil("NACA 2412", chord=1.5, thickness_ratio=0.12, camber=0.02)

print(naca2412)
# NACA 2412 | c = 1.50 m | t/c = 12.0% | camber = 2.0%

print(repr(naca2412))
# Airfoil(designation='NACA 2412', chord=1.5, thickness_ratio=0.12, camber=0.02)

class PanelMesh:
    """A collection of aerodynamic panels for a panel method solver."""

    def __init__(self, panels):
        self._panels = panels   # a list of Panel objects

    def __len__(self):
        return len(self._panels)

    def __iter__(self):
        return iter(self._panels)

    def __repr__(self):
        return f"PanelMesh({len(self)} panels)"


class AeroForces:
    """Stores aerodynamic forces acting on a body."""

    def __init__(self, lift, drag, side_force):
        self.lift       = lift        # Newtons
        self.drag       = drag        # Newtons
        self.side_force = side_force  # Newtons

    def __add__(self, other):
        return AeroForces(
            lift        = self.lift       + other.lift,
            drag        = self.drag       + other.drag,
            side_force  = self.side_force + other.side_force
        )

    def __repr__(self):
        return (f"AeroForces(lift={self.lift:.1f} N, "
                f"drag={self.drag:.1f} N, "
                f"side_force={self.side_force:.1f} N)")

wing_forces      = AeroForces(lift=250000, drag=18000, side_force=0)
fuselage_forces  = AeroForces(lift=5000,   drag=12000, side_force=0)
tailplane_forces = AeroForces(lift=15000,  drag=3000,  side_force=0)

total_forces = wing_forces + fuselage_forces + tailplane_forces

print(total_forces)
# AeroForces(lift=270000.0 N, drag=33000.0 N, side_force=0.0 N)