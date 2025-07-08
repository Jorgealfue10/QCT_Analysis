import numpy as np

def distancia(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def leer_geometrias(file_path):
    geometrías = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        print(lines[i])
        if lines[i].strip().startswith("NR"):
            # Leer las 3 siguientes líneas con coordenadas
            coords = []
            for j in range(2, 5):
                partes = lines[i + j].split()
                print(partes)
                x, y, z = map(float, partes[3:6])
                coords.append((x, y, z))
            geometrías.append(coords)
            i += 4  # Saltar el bloque + línea vacía
        else:
            i += 1  # Por si acaso

    return geometrías

def analizar_geometrias(geometrías):
    for idx, (P, H1, H2) in enumerate(geometrías):
        r_PH1 = distancia(P, H1)
        r_PH2 = distancia(P, H2)
        r_H1H2 = distancia(H1, H2)
	
        with open(f"iccords.dat","a") as f:
            f.write(f"{r_PH1:.6f} {r_PH2:.6f} {r_H1H2:.6f}\n")
        
        print(f"Geometría {idx+1}:")
        print(f"  r(P-H1)  = {r_PH1:.6f} Å")
        print(f"  r(P-H2)  = {r_PH2:.6f} Å")
        print(f"  r(H1-H2) = {r_H1H2:.6f} Å\n")

file = "geoms.xyz"
geos = leer_geometrias(file)
analizar_geometrias(geos)
