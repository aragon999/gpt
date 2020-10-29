#!/usr/bin/env python3
#
# Authors: Christoph Lehner 2020
#          Lorenzo Barca 2020
#   DRAFT
#
import gpt as g
import numpy as np


# load configuration
U = g.load("/glurch/scratch/configs/cls/A653r000/cnfg/A653r000n1750")

# smear the gauge links
alpha, n_iter, blk_max, blk_accuracy = 2.5, 5, 10, 1e-20
g.message("Applying APE-link smearing: \n")
g.message("alpha = {}; n_iter = {}; blk_Max = {}; blk_Accuracy = {}".format(alpha, n_iter, blk_max, blk_accuracy))
params_ape = {"alpha": alpha, "Blk_Max": blk_max, "Blk_Accuracy": blk_accuracy}
U_ape = U
for i in range(5):
    U_ape = g.qcd.gauge.smear.new_ape(U_ape, params_ape)
g.message("Done with APE-link smearing")

# use the gauge configuration grid
grid = U[0].grid
Vol = np.array(grid.fdimensions) # eg [24, 24, 24, 48]
Nt = Vol[-1]
L = Vol[0]

# quark
w = g.qcd.fermion.wilson_clover(U_ape,{
    "kappa" : 0.137,
    "csw_r" : 0.,
    "csw_t" : 0.,
    "xi_0" : 1,
    "nu" : 1,
    "isAnisotropic" : False,
    "boundary_phases" : [ 1.0, 1.0, 1.0, -1.0 ]
})

# create point source
g.message("Creating the point source")
src = g.mspincolor(grid)
g.create.point(src, [0, 0, 0, 26])

# smear the point source
g.message("Applying Wuppertal smearing to the source: kappa = 0.25; steps = 5")
kappa, steps = 0.25, 3
dimensions = [0, 1, 2]
smear = g.create.smear.wuppertal(U, kappa=kappa, steps=steps, dimensions=dimensions)
src_smeared = g(smear * src)
g.message("Done with Wuppertal smearing to the source")

# build solver using g5m and cg
inv = g.algorithms.inverter
pc = g.qcd.fermion.preconditioner
cg = inv.cg({"eps": 1e-10, "maxiter": 1000})

slv_eo2 = w.propagator(inv.preconditioned(pc.eo2_ne(), cg))

# propagator
g.message("Starting the inversion")
dst = g.mspincolor(grid)
dst @= slv_eo2 * src_smeared
g.message("Done with the inversion")

# smear the propagator
g.message("Applying Wuppertal smearing to the propagator: kappa = 0.25; steps = 3")
kappa, steps = 0.25, 3
dimensions = [0, 1, 2]
smear = g.create.smear.wuppertal(U, kappa=kappa, steps=steps, dimensions=dimensions)
dst_smeared = g(smear * dst)

quark_prop_1 = dst
quark_prop_2 = dst
quark_prop_3 = dst

# momentum
moms = np.array(([-1,0,0,0], [0,-1,0,0], [0,0,-1,0],
[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0]), dtype=float)
mom = 2.0 * np.pi * moms / L

mom_list = [ "mom_-100", "mom_0-10", "mom_00-1", "mom_000", "mom_100", "mom_010", "mom_001" ]

data_file = 'baryons2pt.h5'
suN = 2

g.message("Baryon spectrum code")

propagators = {"light" : quark_prop_1, "strange" : quark_prop_2, "charm" : quark_prop_3}

#list_propagators = []
#list_propagators.append(propagators[0])
#list_propagators.append(propagators[2])

#print(list_propagators.keys())

params = {"su(n)": suN, "kappa" : 0.137}

g.qcd.baryon_spectrum.baryon_spectrum(data_file, quark_prop_1, quark_prop_2, quark_prop_3, mom, mom_list, params)
