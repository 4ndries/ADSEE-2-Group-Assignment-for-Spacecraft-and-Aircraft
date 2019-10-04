from math import *

#weights
MTOW = 43090*9.81 # [N]
OEW = 24593*9.81   # [N]
Wfuel = 8832*9.81   #[N]

#wing geometry
b = 28.08          # [m]
S = 93.5           # [m*m]
sweep_quarter_chord = 17.45*pi/180   # [rad]
taper_ratio = 0.235

#flight conditions
Vland = 128*0.5044   # [m/s]
density_land = 1.225   # [kg/m/m/m]
viscosity_land = 0.0000179

Vcruise = 414*0.5044   # [m/s]
density_cruise = 0.3796   # [kg/m/m/m]
viscosity_cruise = 0.00001434          # from: https://www.engineeringtoolbox.com/standard-atmosphere-d_604.html


#calculations of more wing geometry
Cr = 2*S/b/(1+taper_ratio)   # [m]
MAC = 2/3*Cr*(1+taper_ratio+taper_ratio*taper_ratio)/(1+taper_ratio)  #[m]
YMAC = b/6*(1+2*taper_ratio)/(1+taper_ratio)   # [m]

#calculation of reynolds numbers
Re_land = density_land*Vland*MAC/viscosity_land
Re_cruise = density_cruise*Vcruise*MAC/viscosity_cruise

print(Re_land, Re_cruise)
print("land, cruise")





