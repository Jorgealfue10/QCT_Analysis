import os
import glob

def extract_bmax_from_cs_analysis(filepath):
    with open(filepath, "r") as f:
        for line in f:
            if "maximum impact parameter for reaction" in line:
                try:
                    return float(line.split()[8])  # Ajusta si cambia el formato
                except (ValueError, IndexError):
                    continue
    return None

def process_energy_folder(energy_folder, parent_results):
    energy_value = float(energy_folder.split("E")[-1])
    cs_file = os.path.join(energy_folder, "cs_analysis.dat")

    if os.path.isfile(cs_file):
        bmax_val = extract_bmax_from_cs_analysis(cs_file)
        if bmax_val is not None:
            parent_results.append((energy_value, bmax_val))

def main():
    parent_results = []

    for energy_folder in sorted(glob.glob("E*")):
        if os.path.isdir(energy_folder):
            process_energy_folder(energy_folder, parent_results)

    # Guardar el archivo resumen en el directorio padre
    if parent_results:
        with open("Bmax_limits_by_energy.dat", "w") as f:
            for energy, bmax in sorted(parent_results):
                f.write(f"{energy:.2f} {bmax:.6f}\n")

main()

