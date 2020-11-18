# load the model
import pk_model as mod
 
# fit the model with mcmc
mc = pc.MCMC(mod)
mc.use_step_method(pc.AdaptiveMetropolis, [kcp, kpc, ke])
mc.sample(iter=2000, burn=1000, thin=20, verbose=1)

