import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Task 3 asks you to set these before creating any figure
mpl.rcParams.update({
    "font.family":     "serif",
    "font.size":       10,
    "axes.labelsize":  11,
    "axes.titlesize":  12,
    "legend.fontsize": 9,
    "lines.linewidth": 1.8,
    "axes.grid":       True,
    "grid.linestyle":  ":",
    "grid.alpha":      0.5,
})

rng = np.random.default_rng(seed=7)

CD0, k = 0.0085, 0.042

alpha_theory = np.linspace(0.0, 14.0, 300)
CL_theory    = 2 * np.pi * np.radians(alpha_theory)
CD_theory    = CD0 + k * CL_theory**2
LD_theory    = CL_theory / CD_theory

alpha_exp = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0])
CL_exp    = 2 * np.pi * np.radians(alpha_exp) + rng.normal(0.0, 0.025, alpha_exp.size)
CD_exp    = CD0 + k * CL_exp**2 + rng.normal(0.0, 0.0008, alpha_exp.size)
LD_exp    = CL_exp / CD_exp
CL_unc    = np.full_like(CL_exp, 0.02)
CD_unc    = np.full_like(CD_exp, 0.0006)

theory_style = dict(color="steelblue", label="Theory")
exp_style    = dict(color="firebrick", fmt="o", capsize=4, markersize=5,
                    linestyle="none", label="Experiment")

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), constrained_layout=True)

# Panel 1: lift curve
axes[0].plot(alpha_theory, CL_theory, **theory_style)
axes[0].errorbar(alpha_exp, CL_exp, yerr=CL_unc, **exp_style)
axes[0].set_xlabel(r"$\alpha$ (deg)")
axes[0].set_ylabel(r"$C_L$")
axes[0].set_title("Lift curve")
axes[0].legend()

# Panel 2: drag polar, CL on the vertical axis
axes[1].plot(CD_theory, CL_theory, **theory_style)
axes[1].errorbar(CD_exp, CL_exp, xerr=CD_unc, yerr=CL_unc, **exp_style)
axes[1].set_xlabel(r"$C_D$")
axes[1].set_ylabel(r"$C_L$")
axes[1].set_title("Drag polar")
axes[1].legend()

# Panel 3: lift-to-drag ratio
axes[2].plot(alpha_theory, LD_theory, **theory_style)
axes[2].errorbar(alpha_exp, LD_exp, yerr=LD_exp * 0.1, **exp_style)
axes[2].set_xlabel(r"$\alpha$ (deg)")
axes[2].set_ylabel(r"$L/D$")
axes[2].set_title("Lift-to-drag ratio")
axes[2].legend()

# Task 2: mark the best operating point
i_best = np.argmax(LD_theory)
print(f"Max L/D = {LD_theory[i_best]:.2f} at alpha = {alpha_theory[i_best]:.2f} deg, "
      f"CL = {CL_theory[i_best]:.3f}")
print(f"Closed form: CL_opt = {np.sqrt(CD0 / k):.3f}, "
      f"(L/D)_max = {1 / (2 * np.sqrt(CD0 * k)):.2f}")

axes[2].axvline(
    alpha_theory[i_best],
    ymin=0.0,
    ymax=1.0,
    color="black",
    linestyle="--",
)# TODO: vertical dashed line on panel 3 at alpha_theory[i_best] (ax.axvline)
axes[2].text(
    alpha_theory[i_best],
    LD_theory[i_best],
    f"Max L/D = {LD_theory[i_best]:.2f}",
    ha="center", #horizontal alignment
    va="bottom", #vertical alignment
    fontsize=10,
    color="black"
) # TODO: text annotation on panel 3 giving the value of the maximum L/D
axes[1].scatter(CD_theory[i_best], CL_theory[i_best], c="yellow", s=50, marker="*", zorder=5)  # TODO: highlight the same point on panel 2 with ax.scatter, using a distinct marker

fig.suptitle("Aerofoil polar: theory against wind tunnel measurements", fontsize=13)

# Task 4: save
plt.savefig("aerofoil_polar.pdf", format="pdf", bbox_inches="tight") # TODO: save as aerofoil_polar.pdf with bbox_inches="tight"
plt.savefig("aerofoil_polar.png", format="png", dpi=300) # TODO: save as aerofoil_polar.png at 300 dpi
plt.show()