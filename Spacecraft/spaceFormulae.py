'''
Remarks: 
- dB conversions are done in the output script, here we still use the normal way of calculating
- I'm putting trailing underscores behind function parameters, to prevent Python from using global variables/functions with the same name
- Do we want to use SNR_req 10 for FSK8 and BER 1e-6? (This is the same in all cases and was read from the graphs provided in the lecture slides. Another way (probably ovecomplicating) is to use a function from the internet, which does underpredict it though)
'''

### imports
import numpy as np
from scipy import special as sp

### constants/variables
k = 1.38e-23    # [J/K]
Re = 6371e3     # [m]
c = 3e8         # [m/s]
de = 146e6      # [m]
mu = 3.986e14   # [m^3/s^2]

### functions
def to_dB(n_, ref_=1):
    '''Converts physical quantities to [dB]
Accepts integers/floats or np arrays and returns a float or np array respectively'''
    return 10*np.log10(n_/ref_)

def from_dB(n_, ref_=1):
    '''Converts [db] to a physical quantity
Accepts integers/floats or np arrays and returns a float or np array respectively'''
    return ref_*10**(n_/10)

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

def S(h_, theta_=np.nan, ds_=np.nan):
    '''Calculates the (worst case) distance between the satellite and a ground station
Accepts all variables in base units:
h = satellite orbit altitude [m]
theta = elongation angle [deg] (optional)
ds = distance between sun and the planet the mission orbits around [m]
Returns (maximum) distance [m]
Remarks: 
- if theta and ds not specified or equal to np.nan, Earth orbit is assumed
- if calculating interplanetary distances, h is not used, so if it is unknown, just fill in 0
'''
    if not (np.isnan(theta_) and np.isnan(ds_)):  # calculate the interplanetary distance
        return np.sqrt(de**2+ds_**2-2*de*ds_*np.cos(theta_*np.pi/180))  # convert theta to rad
    else:
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

def R(Rg_, Dc_, Tdl_, h_, pxs_):
    '''Calculates the required data rate
Accepts all variables in base units:
Rg = spacecraft generated data rate [bit/s]
Dc = duty cycle [-]
Tdl = downlink time ratio [-]
h = orbital altitude [m]
pxs = pixel size [deg]
Returns the required data rate in [bit/s]'''
    T_ = 2*np.pi*np.sqrt((h_+Re)/mu)  # orbital period
    d_ = Re*2*np.pi  # circumference of Earth alias distance scanned
    # lines per second scanned (using small angle approximation)
    lps_= (d_/T_)/(h_*(pxs_/180*np.pi))  # meter per second scanned / meter per pixel
    bpl_ = Rg_*Dc_/Tdl_  # bits per line
    return bpl_*lps_

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

def SNR_req(BER_=1e-6, coding_='FSK8'):
    '''Calculates the required SNR [dB] given a certain encoding and BER
Remark: when using the function to calculate the SNR, it gives a lower bound, so the actual required SNR may be higher'''
    if True:# BER_ == 1e-6 and coding_ == 'FSK8':  # always activated this for now, to make sure that we're using a required SNR of 10, as given in the slides
        return 10
    elif 0<BER_/2<1 and 'FSK8' in coding_:
        return 2/3*sp.erfcinv(BER_/2)**2
    else:
        print("    ERROR: Unknown encoding or Bit Error Rate out of range [0,2]")
        return np.nan  # let it continue but still notify user of error
#        raise ValueError("Unknown encoding or Bit Error Rate out of range [0,2]")


def main():
    '''Calculates the SNR [dB] from input'''
    # the eval() is to allow typing fractions (5/12), scientific notation (3e9)
    # and even to use functions from the script!    
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
                     Ls(lambd(f), S(h)), Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr)),
                     Lr, R(Rg, Dc, Tdl), Ts))

### main
if __name__ == '__main__':
    print(main())
