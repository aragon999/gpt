#!/usr/bin/env python3
#
# Authors: Christoph Lehner 2020
#
# Benchmark Dslash: TODO: add exactly same as Peter DhopEO
#
import gpt as g

g.default.set_verbose("random", False)
rng = g.random("benchmark")

for precision in [g.single, g.double]:
    grid = g.grid(g.default.get_ivec("--grid", [16, 16, 16, 32], 4), precision)
    N = 1000
    Ls = g.default.get_int("--Ls", 12)
    g.message(
        f"""
DWF Dslash Benchmark with
    fdimensions  : {grid.fdimensions}
    precision    : {precision.__name__}
    Ls           : {Ls}
"""
    )

    # Use Mobius operator
    qm = g.qcd.fermion.mobius(
        g.qcd.gauge.random(grid, rng, scale=0.5),
        {
            "mass": 0.08,
            "M5": 1.8,
            "b": 1.5,
            "c": 0.5,
            "Ls": Ls,
            "boundary_phases": [1.0, 1.0, 1.0, 1.0],
        },
    )

    # Source and destination
    src = g.vspincolor(qm.F_grid)
    dst = g.vspincolor(qm.F_grid)

    rng.cnormal(src)

    # Flops
    gauge_otype = qm.U[0].otype
    Nc = gauge_otype.shape[0]
    flops_per_site = 8 * Nc * (7 + 16 * Nc)
    flops = flops_per_site * src.grid.gsites * N
    nbytes = (
        (8 * 2 * 4 * Nc + 8 * 2 * Nc * Nc / Ls + 2 * 4 * Nc)
        * precision.nbytes
        * src.grid.gsites
        * N
    )

    # Warmup
    for n in range(5):
        qm.Dhop.mat(dst, src)

    # Time
    t0 = g.time()
    for n in range(N):
        qm.Dhop.mat(dst, src)
    t1 = g.time()

    # Report
    GFlopsPerSec = flops / (t1 - t0) / 1e9
    GBPerSec = nbytes / (t1 - t0) / 1e9
    g.message(
        f"""{N} applications of Dhop
    Time to complete            : {t1-t0:.2f} s
    Total performance           : {GFlopsPerSec:.2f} GFlops/s
    Effective memory bandwidth  : {GBPerSec:.2f} GB/s"""
    )
