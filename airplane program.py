from math import *

######################################Part 1

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
sweep_LE = atan(tan(sweep_quarter_chord)+Cr*(1-taper_ratio)/2/b)

#calculation of reynolds numbers
Re_land = density_land*Vland*MAC/viscosity_land
Re_cruise = density_cruise*Vcruise*MAC/viscosity_cruise

print(Re_land, Re_cruise)
print("Re of land, cruise")
print()




########################################################### part 2
#get the cls
Wland = OEW + 0.2*Wfuel  #[N]
CLmax = 1.1*2*Wland/density_land/S/Vland/Vland   #  1.1 safety factor like in slides
Clmax = CLmax/(cos(sweep_quarter_chord))**2     #required Cl max at landing conditions if no flaps used

print(CLmax)
print("required CL max at landing conditions")
print()

#flap geometry
flapstart = b/2*0.1    #[m]
flapend = b/2*0.64    # [m]

#rear spar at 0.6c, 0.05c for mechanism, 0.35 left for flaps
Cflap = 0.35    #flap chord [cf/c]
#assume flap fully deflected, angle 40*, then chord increased by cos(40):
flap_angle = 40*pi/180  #[rad]
bigchord = 1+Cflap*cos(flap_angle)  # c'/c when flaps fully deployed (geometrical, not real)
bigchord2 = 1.21    # c'/c from graph, assume single slotted fowler, adsee presentation slide 36 (realistic)


# calculating Swf/S, integration done on paper, coefficients of result are A,B
A = 5.39234345
B = 0.2938/2
reference_area = 2*((A*flapend-B*flapend*flapend)-(A*flapstart-B*flapstart*flapstart))/S

sweep_LE_flaps = atan(tan(sweep_LE)-(1-Cflap)*2*Cr*(1-taper_ratio)/b)

delta_Cl_max = 1.3*bigchord2
delta_CL_max = 0.9*delta_Cl_max*reference_area*cos(sweep_LE_flaps)

print(delta_CL_max)
print("delta CL max of whole wing at full flaps")
print()





