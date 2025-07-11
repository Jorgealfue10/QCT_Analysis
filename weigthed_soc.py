import numpy as np

def get_Elect_PF(Jval,Eval,Temp,kb=0.69503476):
    gJ= 2 * Jval + 1
    PF = gJ * np.exp(-Eval / (kb*Temp))
    return PF

def get_comp(SOstt,triporder,Jval):
    trip_Ap1=0.0
    trip_App1=0.0
    trip_App2=0.0

    for i in range(len(triporder)):
        k=i+3
        if triporder[i] == 1:
            trip_Ap1 += SOstt[k]
        elif triporder[i] == 2:
            trip_App1 += SOstt[k]
        elif triporder[i] == 3:
            trip_App2 += SOstt[k]
    
    gJ=2*Jval+1
    print(trip_Ap1/gJ, trip_App1/gJ, trip_App2/gJ)
    return trip_Ap1/gJ, trip_App1/gJ, trip_App2/gJ

files=['sigma_1TAp.dat', 'sigma_1TApp.dat', 'sigma_2TApp.dat']
triporder=[1,2,3,2,3,1,1,2,3]
Jvalues=[0,1,2,2,2,1,1,2,2]
Evals=[0.0,164.90,469.12]

dat1TAp = np.loadtxt(files[0])
dat1TApp = np.loadtxt(files[1])
dat2TApp = np.loadtxt(files[2])

w1TAp = 0.0
w1TApp = 0.0
w2TApp = 0.0
Zso=0.0
for i in range(len(Evals)):
    Zso += get_Elect_PF(i, Evals[i], 300.0)

for i in range(len(Jvalues)):
    compdat = np.loadtxt("/home/jorgebdelafuente/Doctorado/PH2M/LZ_SOC/state_"+str(i+1)+".dat")

    Jval = Jvalues[i]
    gJ = 2 * Jval + 1
    Eval = Evals[Jval]
    Temp = 300.0  # Temperature in Kelvin
    PF = get_Elect_PF(Jval, Eval, Temp)/ Zso
    
    trip_Ap1, trip_App1, trip_App2 = get_comp(compdat[0,:], triporder, Jval)
    
    w1TAp += trip_Ap1 * PF
    w1TApp += trip_App1 * PF
    w2TApp += trip_App2 * PF

print("Weighted 1TAp:", w1TAp)
print("Weighted 1TApp:", w1TApp)
print("Weighted 2TApp:", w2TApp)
print("Total weighted sum:", w1TAp + w1TApp + w2TApp)
