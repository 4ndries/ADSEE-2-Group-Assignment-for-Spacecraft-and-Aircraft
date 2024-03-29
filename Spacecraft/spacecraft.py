# in this script the tools and calculations for the spacecraft part are collected
# TODO:
# - 

### imports
import sys
import numpy as np
import pandas as pd
from spaceFormulae import *

# if you run the script with parameter -o or --original, you use linkdata_original.xlsx as input
if len(sys.argv) > 1:
    if sys.argv[1] in ['-o', '--original']:
        data = pd.read_excel('original_linkdata.xlsx')
else:
    data = pd.read_excel('linkdata.xlsx')


def link_budget_template(*args):
    P_, Ll_, Gt_, La_, Gr_, Ls_, Lpr_, Lr_, R_1, k_1, Ts_1, SNR_, SNR_req_, SNR_margin_ = [np.round(to_dB(arg), 3) for arg in args]
    return fr'''        \hline
        Parameter & Value $[dB]$ & Unit \\
        \hline \hline
        P & ${P_}$ & $W$ \\
        \hline
        Ll & ${Ll_}$ & $-$ \\
        \hline
        Gt & ${Gt_}$ & $-$ \\
        \hline
        La & ${La_}$ & $-$ \\
        \hline
        Gr & ${Gr_}$ & $-$ \\
        \hline
        Ls & ${Ls_}$ & $-$ \\
        \hline
        Lpr & ${Lpr_}$ & $-$ \\
        \hline
        Lr & ${Lr_}$ & $-$ \\
        \hline
        1/R & ${R_1}$ & $(bit/s)^{-1}$ \\
        \hline
        1/k & ${k_1}$ & $(J/K)^{-1}$ \\
        \hline
        1/Ts & ${Ts_1}$ & $K^{-1}$ \\
        \hline
        Eb/N0 & ${SNR_}$ & $-$ \\
        \hline
        Eb/N0 required & ${SNR_req_}$ & $-$ \\
        \hline \hline
        SNR margin & ${SNR_margin_}$ & $-$ \\
        \hline'''
    
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
    res = data[sc][15]/60  # convert arcminutes to deg
    s_width = data[sc][14]
    bpp = data[sc][16]
    Dc = data[sc][17]
    Tdl = data[sc][18]/24  # hrs/day to ratio of hrs/24h
    Ts = 135  # assuming same value as given in example calculation
    coding = data[sc][19]
    BER = data[sc][20]
    parent = data[sc][21]

    Gt = Gpeak(Dt, lambd(f), etat)
    Gr = Gpeak(Dr, lambd(f), etar)
    Lspace = Ls(lambd(f), S(h, parent, theta, ds))
    Lpointing = Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr))
    R_req = R(res, s_width, bpp, Dc, Tdl, h, parent)
#    print(R_req)
    SNR_has = to_dB(SNR(P, Ll, Gt, La, Gr,
              Lspace, Lpointing,
              Lr, R_req, Ts))
    SNR_required = SNR_req(BER, coding)
    SNR_margin = SNR_has - SNR_required
    print(link_budget_template(P, Ll, Gt, La, Gr, Lspace, Lpointing, Lr, 1/R_req, 1/k, 1/Ts, from_dB(SNR_has), from_dB(SNR_required), from_dB(SNR_margin)))
    print(f'''{sc} has a downlink SNR margin of {np.round(SNR_margin, 3)} dB\n''')

print('='*50)

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
#    Dc = data[sc][17]  # not needed
#    Tdl = data[sc][18]/24  # not needed
    Ts = 135
    coding = data[sc][19]
    BER = data[sc][20]
    parent = data[sc][21]

    Gt = Gpeak(Dt, lambd(f), etat)
    Gr = Gpeak(Dr, lambd(f), etar)
    Lspace = Ls(lambd(f), S(h, parent, theta, ds))
    Lpointing = Lpr(ett, a12(f, Dt))*Lpr(etr, a12(f, Dr))
    R_req = Rg  # Uplink data rate independent of Payload duty cycle and downlink time

    SNR_has = to_dB(SNR(P, Ll, Gt, La, Gr,
              Lspace, Lpointing,
              Lr, R_req, Ts))
    SNR_required = SNR_req(BER, coding)
    SNR_margin = SNR_has - SNR_required
    print(link_budget_template(P, Ll, Gt, La, Gr, Lspace, Lpointing, Lr, 1/R_req, 1/k, 1/Ts, from_dB(SNR_has), from_dB(SNR_required), from_dB(SNR_margin)))
    print(f'''{sc} has an uplink SNR margin of {np.round(SNR_margin, 3)} dB\n''')
