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
