#!/usr/bin/env python3
"""
TOU Engine (3D Toroidal) — Stress Test Edition (15% Noise)

Restores:
- final_slice.png
- diagnostics.png

No behavioral changes.
"""

from __future__ import annotations
import os, sys, csv, json, math, time
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

@dataclass
class TorusGeom:
    N: int
    R_major: float
    r_minor: float
    cx: float; cy: float; cz: float
    x: np.ndarray; y: np.ndarray; z: np.ndarray
    rho: np.ndarray; d_minor: np.ndarray; mask: np.ndarray

def build_torus(N, R_major_frac, r_minor_frac):
    c = (N - 1) / 2.0
    zz, yy, xx = np.mgrid[0:N, 0:N, 0:N]
    x, y, z = xx - c, yy - c, zz - c
    rho = np.sqrt(x*x + y*y)
    Rm, rm = R_major_frac * N, r_minor_frac * N
    d = np.sqrt((rho - Rm)**2 + z*z)
    mask = d <= rm
    return TorusGeom(N, Rm, rm, c, c, c, x, y, z, rho, d, mask)

def laplacian_3d(u):
    return (-6*u +
        np.roll(u,1,0)+np.roll(u,-1,0)+
        np.roll(u,1,1)+np.roll(u,-1,1)+
        np.roll(u,1,2)+np.roll(u,-1,2))

def grad_3d(u):
    dz = 0.5*(np.roll(u,-1,0)-np.roll(u,1,0))
    dy = 0.5*(np.roll(u,-1,1)-np.roll(u,1,1))
    dx = 0.5*(np.roll(u,-1,2)-np.roll(u,1,2))
    return dx, dy, dz

def ring_source(g, sigma):
    s = np.exp(-(g.d_minor**2)/(2*sigma**2)) * g.mask
    return s/s.max() if s.max() > 0 else s

def run(
    N=121, steps=10000, dt=0.14, c=1.0,
    ping_every=220, ping_amp=2.0,
    reinject_gain=1.0, accumulator_leak=0.015,
    k=0.0035, phase_alpha=0.12,
    noise_amp=0.15, noise_ramp_steps=8000
):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = f"outputs/run_STRESS_{ts}"
    os.makedirs(run_dir+"/slices", exist_ok=True)

    geom = build_torus(N, 0.32, 0.12)
    src = ring_source(geom, 2.4)
    reinject_shape = ring_source(geom, 2.76)
    band = (np.abs(geom.d_minor - 7.0) <= 2.5) & geom.mask

    u = np.zeros((N,N,N))
    u_prev = np.zeros_like(u)
    u += ping_amp * src
    u *= geom.mask

    acc = 0.0
    phase_ema = 0.0
    rng = np.random.default_rng()

    iz0, iy0, ix0 = int(geom.cz), int(geom.cy), int(geom.cx + geom.R_major)

    thetas = np.linspace(0, 2*math.pi, 64, endpoint=False)
    piz = np.full(64, iz0)
    piy = np.clip(np.rint(geom.cy + geom.R_major*np.sin(thetas)).astype(int),0,N-1)
    pix = np.clip(np.rint(geom.cx + geom.R_major*np.cos(thetas)).astype(int),0,N-1)

    # figures
    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(u[N//2], origin="lower")

    # logs
    mf = open(run_dir+"/metrics.csv","w",newline="")
    pf = open(run_dir+"/ring_probes.csv","w",newline="")
    wm, wp = csv.writer(mf), csv.writer(pf)
    wm.writerow(["step","E","acc","inj"])
    wp.writerow(["step"]+[f"p{i:02d}" for i in range(64)])

    E_hist, acc_hist, inj_hist = [], [], []

    t0 = time.time()
    for t in range(steps):
        u_next = (2*u - u_prev) + (c*dt)**2 * laplacian_3d(u)
        u_next *= geom.mask

        ramp = min(1.0, t/noise_ramp_steps)
        u_next += noise_amp*ramp*rng.standard_normal(u.shape)*geom.mask

        u_t = (u_next - u_prev)/(2*dt)
        dx, dy, dz = grad_3d(u)

        r = np.where(geom.rho==0,1.0,geom.rho)
        d = np.where(geom.d_minor==0,1.0,geom.d_minor)

        du_dd = ((dx*geom.x/r + dy*geom.y/r)*((geom.rho-geom.R_major)/d) + dz*(geom.z/d))
        inward = -np.minimum(-u_t*du_dd,0.0)
        acc = (1-accumulator_leak)*acc + inward[band].mean()

        phase_ema = (1-phase_alpha)*phase_ema + phase_alpha*float(u_t[iz0,iy0,ix0])
        inj = math.tanh(k*acc)

        u_next += reinject_gain*inj*math.copysign(1.0,phase_ema+1e-9)*reinject_shape
        u_next *= geom.mask

        if ping_every and t>0 and t%ping_every==0:
            u_next += ping_amp*src
            u_next *= geom.mask

        if t % 10 == 0:
            E = float((u_t*u_t + c*c*(dx*dx+dy*dy+dz*dz))[geom.mask].mean())
            wm.writerow([t,E,acc,inj])
            wp.writerow([t]+u_next[piz,piy,pix].tolist())
            E_hist.append(E)
            acc_hist.append(acc)
            inj_hist.append(inj)
            sys.stdout.write(f"\r15% STRESS | {t:5d}/{steps} | E={E:.2e}")
            sys.stdout.flush()

        if t % 100 == 0:
            im.set_data(u_next[N//2])
            fig.savefig(run_dir+f"/slices/frame_{t:06d}.png")

        u_prev, u = u, u_next

    mf.close(); pf.close()

    # final slice
    ffig, fax = plt.subplots(figsize=(6,6))
    fim = fax.imshow(u[N//2], origin="lower")
    fax.set_title("Final TOU Slice (15% Stress)")
    plt.colorbar(fim, ax=fax)
    ffig.savefig(run_dir+"/final_slice.png", dpi=150)
    plt.close(ffig)

    # diagnostics
    dfig, dax = plt.subplots(figsize=(10,3))
    dax.plot(E_hist,label="E")
    dax.plot(acc_hist,label="acc")
    dax.plot(inj_hist,label="inj")
    dax.legend()
    dax.set_title("TOU Diagnostics — 15% Stress")
    dfig.savefig(run_dir+"/diagnostics.png", dpi=150)
    plt.close(dfig)

    with open(run_dir+"/run_meta.json","w") as f:
        json.dump({"steps":steps,"noise_amp":noise_amp},f,indent=2)

    print(f"\nDone in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
