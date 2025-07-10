import numpy as np

def read_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    return lines

def parse_SOCcomp(lines,nstts,ngeoms):
    SOCcomp= np.zeros((ngeoms, nstts, nstts))    
    geom_index = -1
    nreps = nstts // 8
    if nstts % 8 != 0:
        nreps += 1
    print(nreps)
    start_parse = False
    for i in range(len(lines)):
        if "Composition" in lines[i] and "Total" in lines[i+2]:
            geom_index += 1
            nrep=0
            start_parse = True
        
        if start_parse:
            if "Nr Sym  State" in lines[i] and nrep <= nreps-1:
                m = i + 2
                for j in range(m, m + nstts):
                    if nrep < nreps-1:
                        parts= lines[j].split()
                        l=0
                        for k in range(nrep*8, nrep*8 + 8):
                            print(parts,j,m,nrep,k,l,parts[l+6].rstrip('%'),geom_index)
                            SOCcomp[geom_index, j - m, k] = float(parts[l+6].rstrip('%'))/100
                            l += 1
                    elif nrep == nreps-1:
                        parts = lines[j].split()
                        print(parts)
                        l = 0
                        for k in range(nrep*8, nstts):
                            SOCcomp[geom_index, j - m, k] = float(parts[l+6].rstrip('%'))/100
                            l += 1
                        start_parse = False
                nrep += 1
    return SOCcomp
                        

lines=read_data('input_cas.out')
ngeoms=29
nstts=9
SOCmat=parse_SOCcomp(lines, nstts, ngeoms)

for j in range(nstts):
    with open(f"state_{j+1}.dat", "w") as f:
        for i in range(ngeoms):
            row = SOCmat[i, :, j]  # columna j de la matriz de la geometría i
            line = " ".join(f"{x:.6f}" for x in row)
            f.write(line + "\n")