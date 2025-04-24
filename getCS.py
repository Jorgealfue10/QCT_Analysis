import os
import glob
import re

def extract_sigma_angstroms(filepath):
    with open(filepath, "r") as f:
        for line in f:
            if "Total reaction cross section" in line and "(Angs^2)" in line:
                match = re.search(r"\(Angs\^2\)\s*=\s*([0-9Ee\+\.-]+)", line)
                if match:
                    try:
                        return float(match.group(1))
                    except ValueError:
                        continue
    return None

def process_energy_folder(energy_folder, results):
    try:
        energy_value = float(energy_folder.split("E")[-1])
    except ValueError:
        return
    filepath = os.path.join(energy_folder, "cs_analysis.dat")
    if os.path.isfile(filepath):
        sigma_ang = extract_sigma_angstroms(filepath)
        if sigma_ang is not None:
            results.append((energy_value, sigma_ang))

def main():
    results = []
    for energy_folder in sorted(glob.glob("E*")):
        if os.path.isdir(energy_folder):
            process_energy_folder(energy_folder, results)

    if results:
        with open("sigma_by_energy.dat", "w") as f:
            for energy, sigma in sorted(results):
                f.write(f"{energy:.2f} {sigma:.6f}\n")

if __name__ == "__main__":
    main()

