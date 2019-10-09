# in this script the tools and calculations for the spacecraft part are collected
# TODO:
# - original and modified linkdata.xlsx

### imports
import numpy as np
import pandas as pd
from spaceFormulae import *

data = pd.read_excel(r'linkdata.xlsx')

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
    Rg = data[sc][14]/(data[sc][15]/21600)*data[sc][16]  # convert arcminutes to deg
    Dc = data[sc][17]
    Tdl = data[sc][18]/24  # hrs/day to ratio of hrs/24h
    Ts = 135  # assuming same value as given in example calculation
    coding = 'FSK'+str(data[sc][19])
    BER = data[sc][20]
    SNR_has = to_dB(SNR(P, Ll, Gpeak(Dt, lambd(f), etat), La, Gpeak(Dr, lambd(f), etar),
              Ls(lambd(f), S(h, theta, ds)), Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr)),
              Lr, R(Rg, Dc, Tdl), Ts))
    SNR_margin = SNR_has - SNR_req(BER, coding)
    print(f'''{sc} has a downlink SNR margin of {SNR_margin} dB''')

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
    SNR_has = to_dB(SNR(P, Ll, Gpeak(Dt, lambd(f), etat), La, Gpeak(Dr, lambd(f), etar),
              Ls(lambd(f), S(h, theta, ds)), Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr)),
              Lr, R(Rg, Dc, Tdl), Ts))
    SNR_margin = SNR_has - SNR_req(BER, coding)
    print(f'''{sc} has an uplink SNR margin of {SNR_margin} dB''')
