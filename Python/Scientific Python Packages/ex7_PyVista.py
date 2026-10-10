import numpy as np
import pyvista as pv

b_semi, c_root, c_tip, sweep = 17.5, 6.5, 1.8, np.radians(27.0)

xi = np.linspace(0.0, 1.0, 60)  # chordwise, 0 at leading edge
y = np.linspace(0.0, b_semi, 40)  # spanwise
XI, Y = np.meshgrid(xi, y, indexing="ij")

chord = c_root - (c_root - c_tip) * (Y / b_semi)
X = Y * np.tan(sweep) + XI * chord
Z = np.zeros_like(X)

wing = pv.StructuredGrid(X, Y, Z)
Cp = -1.4 * (1 - XI) ** 0.5 * np.exp(-1.5 * XI) * (1 - (Y / b_semi) ** 2) ** 0.4
wing["Cp"] = Cp.ravel(order="F")

print(wing.n_points, wing.n_cells, Cp.min(), Cp.max())

plotter = pv.Plotter()
plotter.add_mesh(
    wing,
    scalars="Cp",
    cmap="RdBu_r",
    clim=(-1.5, 0.5),
    smooth_shading=True,
    scalar_bar_args={"title": "Cp"},
)
plotter.add_axes()
plotter.show()

off = pv.Plotter(off_screen=True, window_size=(1600, 900))
off.add_mesh(wing, scalars="Cp", cmap="RdBu_r", clim=(-1.5, 0.5))
off.show(screenshot="wing_pressure.png")
wing.save("wing_surface.vtp")