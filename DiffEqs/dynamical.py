import theano.tensor as tt
import theano
from pymc3.distributions import distribution
import fnstep
import pymc3 as pm

floatX='float32' # This is just to fix an annoying casting issue that comes up when using scan

class Dynamical(distribution.Continuous):

    def __init__(self,coeff,sd,x0,y,*args,**kwargs):
#         super(Dynamical,self).__init__(*args,**kwargs)
        super().__init__(*args,**kwargs)
        self.coeff = tt.as_tensor_variable(coeff)
        self.sd    = tt.as_tensor_variable(sd)
        self.x0    = tt.as_tensor_variable(x0)
        self.y     = tt.as_tensor_variable(y)
    
    # The uses of tt.cast are just to fix casting mismatches between float32 and float64 variables
    def get_mu(self,x,x0,coeff,y):
        # Here, we are saying that the vector mu is calculated by iteratively applying 
        # the forward equation 'fn_step' and that it uses external sequence 'y'
        # along with initial value 'coeff' (i.e. a scalar and non-sequence variable).
        # The info about the output is the initial value 'x0'.
        mu,_ = theano.scan(fn = fnstep.fn_step, outputs_info = tt.cast(x0,floatX),
                     non_sequences=tt.cast(coeff,floatX),
                           sequences=tt.cast(y,floatX))
        return mu
    
    def logp(self,x):
        mu = self.get_mu(x,self.x0,self.coeff,self.y)
        sd = self.sd 
        return tt.sum(pm.Normal.dist(mu = mu,sd = sd).logp(x))
