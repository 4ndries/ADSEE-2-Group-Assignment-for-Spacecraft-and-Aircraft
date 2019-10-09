# in this script the tools and calculations for the spacecraft part are collected


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
    ett = data[sc][11]
    etr = 0.1*a12(f, Dr)  # assuming the same relation as in the example calculation
    Rg = data[sc][13]/(data[sc][14]/21600)*data[sc][15]  # convert arcminutes to deg
    Dc = data[sc][16]
    Tdl = data[sc][17]/24  # hrs/day to ratio of hrs/24h
    Ts = 135  # assuming same value as given in example calculation
    print(f'''{sc} has a downlink SNR of {to_dB(SNR(P, Ll, Gpeak(Dt, lambd(f), etat), La, Gpeak(Dr, lambd(f), etar),
                    Ls(lambd(f), S(h)), Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr)),
                    Lr, R(Rg, Dc, Tdl), Ts))} dB''')

