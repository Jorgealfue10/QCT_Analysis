import numpy as np

archivos = ['sigma_1TAp.dat', 'sigma_1TApp.dat', 'sigma_2TApp.dat']

dat1TAp = np.loadtxt(archivos[0])
dat1TApp = np.loadtxt(archivos[1])
dat2TApp = np.loadtxt(archivos[2])

aver = np.zeros(len(dat1TApp[:,0]))
energia = dat1TApp[:,0] 
for i in range(len(dat1TApp[:,0])):
    if dat1TAp[i,0] <= 4.0 and dat1TApp[i,0] <= 4.0 and dat2TApp[i,0] <= 4.0:
        aver[i] = (dat1TAp[i,1] + dat1TApp[i,1] + dat2TApp[i,1]) / 3.0

# Guardar resultado
resultado = np.column_stack((energia, aver))
np.savetxt('meanCS.dat', resultado, header='Energía (eV)    Mean CS (A^2)')

