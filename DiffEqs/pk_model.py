import pymc3 as pc
import numpy as np
from scipy.integrate import odeint
 
time = np.linspace(0, 5, 10)
cc_data = np.array([1.000e+00, 1.613e-01, 5.576e-02, 2.583e-02, 1.264e-02,
6.243e-03, 3.086e-03, 1.525e-03, 7.543e-04, 3.729e-04])
cp_data = np.array([0., 0.1218, 0.0690, 0.0347, 0.0172,
0.0085, 0.00421, 0.0020, 0.0010, 0.00050])

with pc.Model() as model:
    kcp = pc.Uniform('kcp', 0.0, 10.)
    kpc = pc.Uniform('kpc', 0.0, 10.)
    ke = pc.Uniform('ke' , 0.0, 10.)
 
tspan = time
y0 = [cc_data[0], cp_data[0]]
 
# deterministic compartmental model
# @pc.deterministic
def PK(k1=kcp, k2=kpc, k3=ke):
    def pk_model(y, t):
        y_cc, y_cp = y[0], y[1]
        dcc_dt = k1.item() * y_cp - (k2.item() + k3.item()) * y_cc
        dcp_dt = k2.item() * y_cc - k1.item() * y_cp
        dydt = [dcc_dt, dcp_dt]
        return dydt
    soln = odeint(pk_model, y0, tspan)
    cc, cp = soln[:,0], soln[:,1]
    return [cc, cp]
cc = pc.Lambda('cc', lambda PK=PK: PK[0])
cp = pc.Lambda('cp', lambda PK=PK: PK[1])
 
prec = pc.Gamma('precision', alpha=0.1, beta=0.1)
 
# data likelihood
A = pc.Normal('A', mu=cc, tau=prec, value=cc_data, observed=True)
B = pc.Normal('B', mu=cp, tau=prec, value=cp_data, observed=True)
