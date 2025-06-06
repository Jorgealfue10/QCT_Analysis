import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm

def get_BoltzDis(J, Be, T):
    k_B = 0.69503476  # cm^-1/K
    return (2 * J + 1) * np.exp(- (Be * J * (J + 1)) / (k_B * T))

def get_EJ(J, Be):
    return Be * J * (J + 1)

# Constante rotacional
Be_D2 = 0.0037912 * 8065.54429  # cm^-1

# Parámetros
nTemps = 501
nJ = 11
temps = np.arange(1, nTemps + 1)

# Arrays
sum_QJ = np.zeros(nTemps)
Jvals = np.zeros((nTemps, nJ))
EJvals = np.array([get_EJ(J, Be_D2) for J in range(nJ)])

# Cálculo distribución
for i, T in enumerate(temps):
    for J in range(nJ):
        boltz = get_BoltzDis(J, Be_D2, T)
        sum_QJ[i] += boltz
        Jvals[i, J] = boltz

# Normalización
Jvals /= sum_QJ[:, np.newaxis]

colors = cm.tab10(np.linspace(0, 1, nJ))  # Usa viridis, pero puedes cambiarla

# Plot
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# Gráfico de niveles de energía
for J in range(nJ):
    ax1.hlines(EJvals[J], 0, 1, linestyle='-', lw=2, color=colors[J])
ax1.set_xticks([])
ax1.set_ylabel("Energy (cm⁻¹)",fontsize=14)
ax1.tick_params(axis='both', which='major', labelsize=14)

# Gráfico de distribuciones
for J in range(nJ):
    if Jvals[299, J] < 1e-2:
        ax2.plot(temps, Jvals[:, J], color=colors[J])
    else:
        ax2.plot(temps, Jvals[:, J], label=f'J={J}', color=colors[J])

ax2.vlines(300, 0, 1, color="black", linestyle='--', lw=2)
ax2.set_xlabel("Temperature (K)",fontsize=14)
ax2.set_ylabel("Normalized Population",fontsize=14,rotation=-90,labelpad=20)
ax2.tick_params(axis='both', which='major', labelsize=14)
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.legend()

fig.tight_layout()
fig.savefig('Boltzmann_Distribution_D2.png', dpi=300)
plt.show()
