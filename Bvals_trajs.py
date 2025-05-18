import os
import glob

def extract_values_from_cs_analysis(filepath):
    bmax_line_val = None
    bmax_inline_val = None

    with open(filepath, "r") as f:
        for line in f:
            if "maximum impact parameter for reaction CA" in line:
                try:
                    bmax_line_val = float(line.split()[8])
                except (ValueError, IndexError):
                    pass
            elif "BMAX=" in line:
                try:
                    parts = line.split("BMAX=")[1]
                    bmax_inline_val = float(parts.split()[0])
                except (ValueError, IndexError):
                    pass

    return bmax_inline_val, bmax_line_val

def process_energy_folder(energy_folder, parent_results):
    energy_value = float(energy_folder.split("E")[-1])
    cs_file = os.path.join(energy_folder, "cs_analysis.dat")

    if os.path.isfile(cs_file):
        bmax_inline_val, bmax_line_val = extract_values_from_cs_analysis(cs_file)
        if bmax_inline_val is not None and bmax_line_val is not None:
            parent_results.append((energy_value, bmax_inline_val, bmax_line_val))

def main():
    parent_results = []

    for energy_folder in sorted(glob.glob("E*")):
        if os.path.isdir(energy_folder):
            process_energy_folder(energy_folder, parent_results)

    # Guardar el archivo resumen
    if parent_results:
        with open("Bmax_limits_by_energy.dat", "w") as f:
            f.write("Energy  BMAX  MaxImpactParam\n")
            for energy, bmax1, bmax2 in sorted(parent_results):
                f.write(f"{energy:.2f} {bmax1:.6f} {bmax2:.6f}\n")

main()
