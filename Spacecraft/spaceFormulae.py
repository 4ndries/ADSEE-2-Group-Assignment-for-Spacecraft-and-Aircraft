'''
Hereby the variables used in formulae are explained:

Tc -- temperature of the noise introduced by the cable
T0 -- clarify later; given OR reference temperature IF reference, T0 = 290 K
L  -- loss factor, property of a cable
Tn -- temperature of the noise introduced by the amplifier
F  -- noise figure, ratio of noise out to noise into the amp

There are different typical values of antenna noise, L, F, etc. for different frequencies
for downlink/uplink => we need to have a table with different options to get the right values

'''
### imports
import math as m
import numpy as np

### constants/variables
k = 1.38e-23    # [J/K]
Re = 6371000    # [m]
c = 3e8         # [m/s]

### functions
def to_dB(n, ref=1):
    '''Accepts integers/floats and numpy arrays and returns a float or a numpy array respectively'''
    return 10*np.log10(n/ref)



def SNR(P, Ll, Gt, La, Gr, Ls, Lpr, Lr, R, Ts):
    '''Accepts all variables from the link budget equation:
P = transmitter power
Ll = transmitter loss factor
Gt = transmitter gain'''
    return
