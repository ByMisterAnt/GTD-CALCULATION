import math
#import numpy as np
import matplotlib.pyplot as plt

"""
def input_data():
    return M, H, sigmaVH, Gpr, Pn, Tn, an, k, Vp, lyambda, tau, pi
    """
Mp = 2
H = 5000
sigmaVH = -0.169714286*Mp+1.213523810
if sigmaVH > 1:
    sigmaVH = 1

###############
sigmaVH = 0.97
###############


Gpr = 26
Pn = 54016.92
Tn = 255.6
an = 320.4058
k = 1.4
kg = 1.33
Tg = 1600
sigmaKS = 0.95
kpdTK = 0.9
kpdTTK = 0.99
delta_ohl = 0.05
m = 0.6
kpdTV = 0.9
kpdTTV = 0.99

def q_function(k, lyambda):
    return math.pow((k+1)/2, 1/(k-1))*lyambda*math.pow(1-(k-1)/(k+1)*lyambda**2, 1/(k-1))

Vp = Mp*an
lyambda = math.sqrt( ( ((k+1)/2)*Mp**2 ) / (1+(((k-1)/2)*Mp**2)) )
tau = 1-(k-1)/(k+1)*lyambda**2
pi = math.pow(tau,k/(k-1))
#
#print(pi, "\t", tau, "\t", lyambda, "\t",sigmaVH)
#++
#############################################################################
#Bx

Pvh = Pn*sigmaVH/pi
Tvh = Tn/tau

q = pow((k+1)/2,1/(k-1))*lyambda*pow(tau,1/(k-1))
piV = 2.65*q+0.125
kpdV = 0.5*q+0.5
Pvn = Pvh*piV
Tvn = Tvh*(1+(pow(piV,0.286)-1)/kpdV)
#
#print(Pvh, "\t", Tvh, "\t", q, "\t", piV, "\t", kpdV, "\t", Pvn, Tvn)
#++
#############################################################################
#K
piK = 0.00285804*Gpr**2+0.038630653*Gpr+1.581155779
kpdK = 0.000052083*Gpr**3-0.0028125*Gpr**2+0.057916667*Gpr+0.38
Pk = Pvn*piK
Tk = Tvn*(1+(pow(piK,0.286)-1)/kpdK)
#
#print(Pk, "\t", Tk, "\t", piK, "\t", kpdK)
#
#############################################################################
#KC

Pg = Pk*sigmaKS

cpTg = 1.328571429*Tg-390
cpTk = -0.0035*Tg**2+13.549999981*Tg-11449.99998261
cpnTg = 5*Tg-2000
cpnT0 = 455
kpdG = 0.98
Hu = 42900

qT = (cpTg-cpTk)/(Hu*kpdG-cpnTg+cpnT0)
#
#print(qT)
#
#############################################################################
#TK
delta_otb = (1+qT)*delta_ohl/((1+qT)*delta_ohl+1)
Xtk = 1005*(Tk-Tvn)/(1165*Tg*kpdTK*(1+qT)*(1-delta_otb)*kpdTTK)
piTK = pow(1-Xtk,-kg/(kg-1))

Ptk = Pg/piTK
Ttk = Tg*(1-Xtk*kpdTK)
#
#print(Xtk, "\t",piTK, "\t",Ttk,"\t", Ptk, "\n")
#++
#############################################################################
#TB

Xtv = (1005*(1+m)*(Tvn-Tvh)/(1165*Ttk*kpdTV*(1+qT)*(1-delta_otb)*kpdTTV))
piTV = pow(1-Xtv,-kg/(kg-1))
Pt = Ptk/piTV
Tt = Ttk*(1-Xtv*kpdTV)
#
#print(Xtv, "\t",piTV, "\t",Tt,"\t", Pt, "\t")
#++
#############################################################################
#vnytr kontyr

#lyambda_c1 = math.sqrt((1-math.pow(Pn/Pt,(kg-1)/kg))*(kg+1)/(kg-1))
lyambda_c1s = 1
pi_c1s = math.pow(1-(kg-1)*lyambda_c1s**2,kg/(kg-1))
P1cs = Pt*pi_c1s
lyambda_c1 = 0.97
pi_c1 = math.pow(1-(kg-1)*lyambda_c1**2,kg/(kg-1))
P1c = P1cs/pi_c1
#
#print(P1c)
#+-
#############################################################################
Tc = Tt*(1+m*Tvn/Tt)/(1+m)
Pc = (Pvn+P1c)/2
#
#print(Tc, "\t", Pt, "\t", Pc)
#














x=["Н", "B", "BH", "K", "Г", "TK", "T", "C"]
t=[Tn, Tvh, Tvn, Tk, Tg, Ttk, Tt, Tc]
p=[Pn, Pvh, Pvn, Pk, Pg, Ptk, Pt, Pc]
plt.plot(x,p)
plt.grid()
plt.show()
plt.plot(x,t)
plt.grid()
plt.show()
