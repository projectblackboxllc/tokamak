#!/usr/bin/env python3
"""
TOU Tokamak — Magnetic confinement extension of TOU Engine 3D
Adds : safety factor q(r), parallel gradient, coupled density field n.
Keeps: accumulator, phase-sensitive reinjection, 64 ring probes — unchanged.
Project Black Box LLC
"""
from __future__ import annotations
import os, sys, csv, json, math, time
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# ── Geometry ───────────────────────────────────────────────────────────────
@dataclass
class TorusGeom:
    N: int
    R_major: float; r_minor: float
    cx: float; cy: float; cz: float
    x: np.ndarray; y: np.ndarray; z: np.ndarray
    rho: np.ndarray; d_minor: np.ndarray; mask: np.ndarray

def build_torus(N, R_major_frac, r_minor_frac):
    c = (N-1)/2.0
    zz, yy, xx = np.mgrid[0:N, 0:N, 0:N]
    x, y, z = xx-c, yy-c, zz-c
    rho   = np.sqrt(x*x + y*y)
    Rm, rm = R_major_frac*N, r_minor_frac*N
    d     = np.sqrt((rho-Rm)**2 + z*z)
    mask  = d <= rm
    return TorusGeom(N, Rm, rm, c,c,c, x,y,z, rho, d, mask)

# ── Operators ──────────────────────────────────────────────────────────────
def laplacian_3d(u):
    return (-6*u
            + np.roll(u,1,0)+np.roll(u,-1,0)
            + np.roll(u,1,1)+np.roll(u,-1,1)
            + np.roll(u,1,2)+np.roll(u,-1,2))

def grad_3d(u):
    dz = 0.5*(np.roll(u,-1,0)-np.roll(u,1,0))
    dy = 0.5*(np.roll(u,-1,1)-np.roll(u,1,1))
    dx = 0.5*(np.roll(u,-1,2)-np.roll(u,1,2))
    return dx, dy, dz

def parallel_grad(u, g, q):
    """∇_∥ u along field line: (∂_θ + (1/q)∂_φ) / R"""
    d_pol = 0.5*(np.roll(u,-1,0)-np.roll(u,1,0))   # z ≈ poloidal
    d_tor = 0.5*(np.roll(u,-1,1)-np.roll(u,1,1))   # y ≈ toroidal
    R = np.where(g.rho==0, 1.0, g.rho)
    return (d_pol + d_tor/q) / R

def safety_factor(g, q0=1.5, q1=2.0):
    """q(r) = q0 + q1*(r/a)^2  — parabolic profile, q>1 everywhere"""
    r_norm = g.d_minor / g.r_minor
    return np.clip(q0 + q1*r_norm**2, 1.0, None)

def ring_source(g, sigma):
    s = np.exp(-(g.d_minor**2)/(2*sigma**2)) * g.mask
    return s/s.max() if s.max()>0 else s

# ── Run ────────────────────────────────────────────────────────────────────
def run(
    N=81, steps=8000, dt=0.12, c=1.0,
    ping_every=200,  ping_amp=2.0,
    reinject_gain=1.0, accumulator_leak=0.015,
    k=0.0035, phase_alpha=0.12,
    noise_amp=0.15, noise_ramp_steps=5000,
    kappa_n=0.08,   # density-gradient drive
    D_diff=0.02,    # density diffusion
    q0=1.5, q1=2.0  # safety factor
):
    ts      = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = f"outputs/tokamak_{ts}"
    os.makedirs(run_dir, exist_ok=True)

    geom  = build_torus(N, 0.32, 0.12)
    q     = safety_factor(geom, q0, q1)
    src   = ring_source(geom, 2.4)
    rinj  = ring_source(geom, 2.76)
    scale = N/121.0
    band  = (np.abs(geom.d_minor - 7.0*scale) <= 2.5*scale) & geom.mask

    # Two fields: φ (potential / wave) and n (density perturbation)
    u      = ping_amp * src
    u_prev = np.zeros_like(u)
    n      = np.zeros_like(u)

    acc = 0.0; phase_ema = 0.0
    rng = np.random.default_rng()

    iz0 = int(geom.cz)
    iy0 = int(geom.cy)
    ix0 = int(np.clip(geom.cx + geom.R_major, 0, N-1))

    thetas = np.linspace(0, 2*math.pi, 64, endpoint=False)
    piz = np.full(64, iz0, dtype=int)
    piy = np.clip(np.rint(geom.cy + geom.R_major*np.sin(thetas)).astype(int), 0, N-1)
    pix = np.clip(np.rint(geom.cx + geom.R_major*np.cos(thetas)).astype(int), 0, N-1)

    mf = open(run_dir+"/metrics.csv",  "w", newline="")
    pf = open(run_dir+"/ring_probes.csv","w", newline="")
    wm, wp = csv.writer(mf), csv.writer(pf)
    wm.writerow(["step","E_phi","E_n","acc","inj"])
    wp.writerow(["step"]+[f"p{i:02d}" for i in range(64)])

    E_hist=[]; En_hist=[]; acc_hist=[]; inj_hist=[]
    t0 = time.time()

    for t in range(steps):
        # ── φ (wave/potential) — driven by density via parallel gradient ──
        par_n  = parallel_grad(n, geom, q)
        u_next = (2*u - u_prev) + (c*dt)**2 * laplacian_3d(u) + dt**2*kappa_n*par_n
        u_next *= geom.mask

        # ── n (density) — driven by parallel gradient of φ ──
        par_u  = parallel_grad(u, geom, q)
        n_next = n + dt*(-kappa_n*par_u + D_diff*laplacian_3d(n))
        n_next *= geom.mask

        # ── Noise (same ramp as original) ──
        ramp  = min(1.0, t/noise_ramp_steps)
        noise = noise_amp*ramp*rng.standard_normal(u.shape)*geom.mask
        u_next += noise
        n_next += 0.3*noise

        # ── TOU Accumulator — identical mechanism ──
        u_t  = (u_next - u_prev)/(2*dt)
        dx, dy, dz = grad_3d(u)
        r    = np.where(geom.rho==0,    1.0, geom.rho)
        d    = np.where(geom.d_minor==0, 1.0, geom.d_minor)
        du_dd = ((dx*geom.x/r + dy*geom.y/r)*((geom.rho-geom.R_major)/d)
                 + dz*(geom.z/d))
        inward   = -np.minimum(-u_t*du_dd, 0.0)
        acc      = (1-accumulator_leak)*acc + inward[band].mean()
        phase_ema = (1-phase_alpha)*phase_ema + phase_alpha*float(u_t[iz0,iy0,ix0])
        inj      = math.tanh(k*acc)

        # ── Phase-sensitive reinjection — identical mechanism ──
        u_next += reinject_gain*inj*math.copysign(1.0, phase_ema+1e-9)*rinj
        u_next *= geom.mask

        if ping_every and t>0 and t%ping_every==0:
            u_next += ping_amp*src
            u_next *= geom.mask

        if t%10==0:
            E  = float((u_t**2 + c**2*(dx**2+dy**2+dz**2))[geom.mask].mean())
            En = float((n_next**2)[geom.mask].mean())
            wm.writerow([t, E, En, acc, inj])
            wp.writerow([t]+u_next[piz,piy,pix].tolist())
            E_hist.append(E); En_hist.append(En)
            acc_hist.append(acc); inj_hist.append(inj)
            sys.stdout.write(
                f"\rTOKAMAK | {t:5d}/{steps} | "
                f"E={E:.2e} En={En:.2e} inj={inj:.4f}"
            )
            sys.stdout.flush()

        u_prev, u, n = u, u_next, n_next

    mf.close(); pf.close()

    # ── Output plots ───────────────────────────────────────────────────────
    ffig, axes = plt.subplots(1, 2, figsize=(12,5))
    ffig.patch.set_facecolor("#0d0d0d")
    for ax in axes:
        ax.set_facecolor("#0d0d0d")
        ax.tick_params(colors="#aaaaaa")
        for sp in ax.spines.values(): sp.set_edgecolor("#333333")

    im0 = axes[0].imshow(u[N//2], origin="lower", cmap="RdBu_r")
    axes[0].set_title("φ — Potential (final slice)", color="white")
    plt.colorbar(im0, ax=axes[0])

    im1 = axes[1].imshow(n[N//2], origin="lower", cmap="plasma")
    axes[1].set_title("n — Density perturbation (final slice)", color="white")
    plt.colorbar(im1, ax=axes[1])

    ffig.suptitle(f"TOU Tokamak  |  q₀={q0}  q₁={q1}  κₙ={kappa_n}",
                  color="white", fontsize=11)
    ffig.savefig(run_dir+"/final_slice.png", dpi=150,
                 bbox_inches="tight", facecolor=ffig.get_facecolor())
    plt.close(ffig)

    dfig, dax = plt.subplots(figsize=(10,3))
    dfig.patch.set_facecolor("#0d0d0d")
    dax.set_facecolor("#0d0d0d")
    dax.tick_params(colors="#aaaaaa")
    dax.plot(E_hist,   color="#00c8ff", label="E(φ)")
    dax.plot(En_hist,  color="#ff4444", label="E(n)")
    dax.plot(acc_hist, color="#ffaa00", label="acc")
    dax.plot(inj_hist, color="#44ff88", label="inj")
    dax.legend(facecolor="#1a1a1a", labelcolor="#cccccc")
    dax.set_title("TOU Tokamak — Diagnostics", color="white")
    dfig.savefig(run_dir+"/diagnostics.png", dpi=150,
                 bbox_inches="tight", facecolor=dfig.get_facecolor())
    plt.close(dfig)

    with open(run_dir+"/run_meta.json","w") as f:
        json.dump({"steps":steps,"N":N,"noise_amp":noise_amp,
                   "q0":q0,"q1":q1,"kappa_n":kappa_n,"D_diff":D_diff}, f, indent=2)

    print(f"\nDone in {time.time()-t0:.1f}s  →  {run_dir}")

if __name__=="__main__":
    run()
