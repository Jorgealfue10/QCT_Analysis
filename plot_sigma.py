import numpy as np
import matplotlib.pyplot as plt
import os

# Constants
def get_CS(file_path):
    return np.loadtxt(file_path)

def get_BoltzDis(J, Be, T):
    k_B = 0.69503476  # Boltzmann constant in eV/K
    return (2 * J + 1) * np.exp(- (Be * J * (J + 1)) / (k_B * T))

def get_EJ(J, Be):
    return Be * J * (J + 1)

Be_D2 = 0.0037912 * 8065.54429
nJ = 11
temp = 300.

# Calculate normalized Boltzmann weights
sum_QJ = 0.
Jvals = np.zeros(nJ)
EJvals = np.zeros(nJ)
for J in range(nJ):
    weight = get_BoltzDis(J, Be_D2, temp)
    sum_QJ += weight
    Jvals[J] = weight
    EJvals[J] = get_EJ(J, Be_D2)
Jvals /= sum_QJ

# Initialize plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel(r"E$_{col}$ (eV)", fontsize=14)
ax.set_ylabel(r"Cross Section ($\AA^2$)", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=14)

# Read and plot cross sections
sum_sigma = None
energies = None

eigenvalj=[0.191,0.199,0.213,0.235,0.265,0.301,0.344]

for J in range(7):
    file_path = f"J{J}/sigma_by_energy.dat"
    if os.path.exists(file_path):
        try:
            sigma = get_CS(file_path)
            energy = sigma[:, 0]+eigenvalj[J]
            energy = sigma[:, 0] #+eigenvalj[J]
            cs = sigma[:, 1]
            weighted_cs = cs * Jvals[J]
            if sum_sigma is None:
                sum_sigma = weighted_cs.copy()
                energies = energy.copy()
            else:
                sum_sigma += weighted_cs
            ax.plot(energy, cs, label=f'j={J}')
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Plot total weighted sum
if sum_sigma is not None and energies is not None:
    ax.plot(energies, sum_sigma, label='Weighted sum of j=0-6', color='black', linestyle='--', lw=2)

if sum_sigma is not None and energies is not None:
    output_data = np.column_stack((energies, sum_sigma))
    np.savetxt("weighted_sum_sigma.dat", output_data, header="Energy (eV)    Weighted Cross Section (a.u.)")
    print("Guardado en 'weighted_sum_sigma.dat'")


ax.legend(frameon=False, fontsize=12)
fig.tight_layout()
fig.savefig("cs_wJ_v2.png",dpi=300,transparent=True)

plt.show()
