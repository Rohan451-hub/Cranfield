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