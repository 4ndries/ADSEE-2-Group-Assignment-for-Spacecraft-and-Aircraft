# in this script the tools and calculations for the spacecraft part are collected
# TODO:
# - 

### imports
import numpy as np
import pandas as pd
from spaceFormulae import *

data = pd.read_excel('linkdata.xlsx')
#data = pd.read_excel('original_linkdata.xlsx')

# downlink
for sc in data.columns[2:]:
    P = data[sc][1]
    Ll = data[sc][3]
    Lr = data[sc][4]
    Dt = data[sc][7]
    f = data[sc][5]*1e9  # to convert from GHz to Hz
    etat = 0.55  # assuming same value as given in example calculation
    La = from_dB(-0.5)  # assuming same value as given in example calculation
    Dr = data[sc][8]
    etar = 0.55  # assuming same value as given in example calculation
    h = data[sc][9]*1e3  # to convert from km to m
    theta = data[sc][10]
    ds = data[sc][11]*1e3  # convert km to m
    ett = data[sc][12]
    etr = 0.1*a12(f, Dr)  # assuming the same relation as in the example calculation
    # Include orbital velocity so we know how many rows per second are scanned, instead of one row per second...
    Rg = data[sc][14]/(data[sc][15]/21600)*data[sc][16]  # convert arcminutes to deg
    Dc = data[sc][17]
    Tdl = data[sc][18]/24  # hrs/day to ratio of hrs/24h
    Ts = 135  # assuming same value as given in example calculation
    coding = 'FSK'+str(data[sc][19])
    BER = data[sc][20]

    Gt = Gpeak(Dt, lambd(f), etat)
    Gr = Gpeak(Dr, lambd(f), etar)
    Lspace = Ls(lambd(f), S(h, theta, ds))
    Lpointing = Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr))
    R_req = R(Rg, Dc, Tdl)
    
    SNR_has = to_dB(SNR(P, Ll, Gt, La, Gr,
              Lspace, Lpointing,
              Lr, R_req, Ts))
    SNR_required = SNR_req(BER, coding)
    SNR_margin = SNR_has - SNR_required
    print(f'''Downlink budget {sc} [dB]:
P: {to_dB(P)}
Ll: {to_dB(Ll)}
Gt: {to_dB(Gt)}
La: {to_dB(La)}
Gr: {to_dB(Gr)}
Ls: {to_dB(Lspace)}
Lpr: {to_dB(Lpointing)}
Lr: {to_dB(Lr)}
1/R: {to_dB(1/R_req)}
1/k: {to_dB(1/k)}
1/Ts: {to_dB(1/Ts)}
Eb/N0: {SNR_has}
Eb/N0 required: {SNR_required}
margin: {SNR_margin}''')
    print(f'''{sc} has a downlink SNR margin of {np.round(SNR_margin, 3)} dB\n''')

# uplink
for sc in data.columns[2:]:
    P = data[sc][2]
    Ll = data[sc][3]
    Lr = data[sc][4]
    Dt = data[sc][8]
    f = data[sc][5]*1e9 * data[sc][6]  # conversion GHz -> Hz and turnaround ratio
    etat = 0.55
    La = from_dB(-0.5)
    Dr = data[sc][7]
    etar = 0.55
    h = data[sc][9]*1e3
    theta = data[sc][10]
    ds = data[sc][11]*1e3
    ett = 0.1*a12(f, Dt)
    etr = data[sc][12]
    Rg = data[sc][13]
    Dc = data[sc][17]
    Tdl = data[sc][18]/24  # no uplink time given, for now using the downlink time but we'll see
    Ts = 135
    coding = 'FSK'+str(data[sc][19])
    BER = data[sc][20]

    Gt = Gpeak(Dt, lambd(f), etat)
    Gr = Gpeak(Dr, lambd(f), etar)
    Lspace = Ls(lambd(f), S(h, theta, ds))
    Lpointing = Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr))
    R_req = Rg  #R(Rg, Dc, Tdl)  # Uplink data rate independent of Payload duty cycle and downlink time

    SNR_has = to_dB(SNR(P, Ll, Gt, La, Gr,
              Lspace, Lpointing,
              Lr, R_req, Ts))
    SNR_required = SNR_req(BER, coding)
    SNR_margin = SNR_has - SNR_required
    print(f'''Uplink budget {sc} [dB]:
P: {to_dB(P)}
Ll: {to_dB(Ll)}
Gt: {to_dB(Gt)}
La: {to_dB(La)}
Gr: {to_dB(Gr)}
Ls: {to_dB(Lspace)}1
Lpr: {to_dB(Lpointing)}
Lr: {to_dB(Lr)}
1/R: {to_dB(1/R_req)}
1/k: {to_dB(1/k)}
1/Ts: {to_dB(1/Ts)}
Eb/N0: {SNR_has}
Eb/N0 required: {SNR_required}
margin: {SNR_margin}''')
    print(f'''{sc} has an uplink SNR margin of {np.round(SNR_margin, 3)} dB\n''')
