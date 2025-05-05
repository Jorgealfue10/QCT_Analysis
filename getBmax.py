import os
import glob

def extract_bmax(filepath):
    with open(filepath, "r") as f:
        for line in f:
            if "maximum impact parameter for reaction" in line:
                try:
                    return float(line.split()[8])  # Ajusta si cambia el formato
                except (ValueError, IndexError):
                    continue
    return None

def is_valid_b_folder(folder):
    basename = os.path.basename(folder)
    if not basename.startswith("B"):
        return False
    try:
        float(basename[1:])  # Intenta convertir lo que viene después de la "B"
        return os.path.isdir(folder)
    except ValueError:
        return False

def process_energy_folder(energy_folder, parent_results):
    energy_value = float(energy_folder.split("E")[-1])
    bmax_dirs = sorted(
        [b for b in glob.glob(os.path.join(energy_folder, "B*")) if is_valid_b_folder(b)],
        key=lambda x: float(os.path.basename(x).split("B")[-1])
    )

    bvals = []
    ca_vals = []
    found = False

    for b_folder in bmax_dirs:
        b_val = float(os.path.basename(b_folder).split("B")[-1])
        test_file = os.path.join(b_folder, "test_analys.out")
        print(test_file)

        if os.path.isfile(test_file):
            bmax_val = extract_bmax(test_file)
            if bmax_val is not None:
                bvals.append(b_val)
                ca_vals.append(bmax_val)

                diff = b_val - bmax_val
                if not found and diff >= 0.11:
                    parent_results.append((energy_value, b_val, bmax_val*1.0))
                    found = True

    # Guardar los Bmax en cada carpeta E
    if bvals and ca_vals:
        with open(os.path.join(energy_folder, "analyse_Bmax_CA.dat"), "w") as f:
            for b, ca in zip(bvals, ca_vals):
                f.write(f"{b:.2f} {ca:.6f}\n")

def main():
    parent_results = []

    for energy_folder in sorted(glob.glob("E*")):
        print(energy_folder)
        if os.path.isdir(energy_folder):
            process_energy_folder(energy_folder, parent_results)

    # Guardar el archivo resumen en el directorio padre
    if parent_results:
        with open("Bmax_limits_by_energy.dat", "w") as f:
            for energy, bval, bmax in sorted(parent_results):
                f.write(f"{energy:.2f} {bval:.2f} {bmax:.6f}\n")

main()
