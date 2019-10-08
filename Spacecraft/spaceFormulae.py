'''
Hereby the variables used in formulae are explained:

Tc -- temperature of the noise introduced by the cable
T0 -- clarify later; given OR reference temperature IF reference, T0 = 290 K
L  -- loss factor, property of a cable
Tn -- temperature of the noise introduced by the amplifier
F  -- noise figure, ratio of noise out to noise into the amp

There are different typical values of antenna noise, L, F, etc. for different frequencies
for downlink/uplink => we need to have a table with different options to get the right values


Remarks: 
- I'm not using dB (for now), as we don't have to calculate manually anymore
- I'm putting trailing underscores behind function parameters, to prevent Python from using global variables/functions with the same name
'''
### imports
import numpy as np

### constants/variables
k = 1.38e-23    # [J/K]
Re = 6371000    # [m]
c = 3e8         # [m/s]

### functions
def to_dB(n_, ref_=1):
    '''Converts physical quantities to [dB]
Accepts integers/floats or np arrays and returns a float or np array respectively'''
    return 10*np.log10(n_/ref_)

def from_dB(n_, ref_=1):
    '''Converts [db] to a physical quantity
Accepts integers/floats or np arrays and returns a float or np array respectively'''
    return ref_*np.exp(n_/10)

def Gpeak(D_, lambd_, eta_):
    '''Calculates the peak antenna gain
Accepts all variables in base units:
D = antenna diameter [m]
lambd = wavelength [m]
eta = antenna efficiency [-]
Returns antenna peak gain [-]'''
    return (np.pi*D_/lambd_)**2*eta_

def Ls(lambd_, S_):
    '''Calculates the space loss
Accepts all variables in base units:
lambd = wavelength [m]
S = (maximum) distance [m]
Returns space loss [-]'''
    return (lambd_/(4*np.pi*S_))**2

def S(h_):
    '''Calculates the worst case distance between the satellite and a ground station
Accepts all variables in base units:
h = satellite orbit altitude [m]
Returns maximum distance [m]'''
    return np.sqrt((Re+h_)**2-Re**2)

def lambd(f_):
    '''Calculates the wavelength [m] of radiation of a given frequency [Hz]'''
    return c/f_

def Lpr(et_, a12_):
    '''Calculates the pointing loss of an antenna
Accepts all variables in base units:
et = pointing offset [deg]
a12 = half-power angle [deg]
Returns the pointing loss of one antenna [-]
(for the total pointing loss you need to multiply the transmitter and receiver pointing losses)'''
    return from_dB(-12*(et_/a12_)**2)

def a12(f_, D_):
    '''Calculates the half-power angle of an antenna beam
Accepts all variables in base units:
f = signal frequency [Hz]
D = antenna diameter [m]
Returns the half-power angle [deg]'''
    return 21/(f_*D_*1e-9)  # convert Hz to GHz

def R(Rg_, Dc_, Tdl_):
    '''Calculates the required data rate
Accepts all variables in base units:
Rg = spacecraft generated data rate [bit/s]
Dc = duty cycle [-]
Tdl = downlink time ratio [-]
Returns the required data rate in [bit/s]'''
    return Rg_*Dc_/Tdl_

def SNR(P_, Ll_, Gt_, La_, Gr_, Ls_, Lpr_, Lr_, R_, Ts_):
    '''Accepts all variables from the link budget equation:
P = transmitter power [W]
Ll = transmitter loss factor [-]
Gt = transmitter antenna gain [-]
La = transmission path loss [-]
Gr = receiving antenna gain [-]
Ls = space loss [-]
Lpr = antenna pointing loss [-]
Lr = receiver loss factor [-]
R = required data rate [bit/s]
Ts = system noise temperature [K]
Returns Signal-to-Noise-Ratio [-]'''
    return P_*Ll_*Gt_*La_*Gr_*Ls_*Lpr_*Lr_/(R_*k*Ts_)


def main():
    '''Calculates the SNR [dB] from input'''
    # the eval() is to allow typing fractions (5/12), scientific notation (3e9) etc.    
    P = float(eval(input('transmitter power [W]? ')))
    Ll = float(eval(input('transmitter loss factor [-]? ')))
    Dt = float(eval(input('transmitter antenna diameter [m]? ')))
    Dr = float(eval(input('receiver antenna diameter [m]? ')))
    f = float(eval(input('signal frequency [Hz]? ')))
    etat = float(eval(input('transmitter antenna efficiency [-]? ')))
    etar = float(eval(input('receiver antenna efficiency [-]? ')))
    La = from_dB(float(eval(input('transmission path loss [dB]? '))))
    h = float(eval(input('orbit altitude [m]? ')))
    ett = float(eval(input('transmitter pointing offset [deg]? ')))
    etr = float(eval(input('receiver pointing offset [deg]? ')))
    Lr = float(eval(input('receiver loss factor [-]? ')))
    Rg = float(eval(input('spacecraft generated data rate [bit/s]? ')))
    Dc = float(eval(input('duty cycle [-]? ')))
    Tdl = float(eval(input('downlink time ratio [-]? ')))
    Ts = float(eval(input('system noise temperature [K]? ')))
    return to_dB(SNR(P, Ll, Gpeak(Dt, lambd(f), etat), La, Gpeak(Dr, lambd(f), etar),
              Ls(lambd(f), S(h)), Lpr(ett, a12(f, Dt))+Lpr(etr, a12(f, Dr)),
              Lr, R(Rg, Dc, Tdl), Ts)))

if __name__ == '__main__':
    print(main())
