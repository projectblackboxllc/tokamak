#!/usr/bin/env python3
"""Render a single frames.json into an MP4 animation.

Usage:
    python3 videos/render_frames.py <path/to/frames.json> [output.mp4]

If matplotlib's ffmpeg writer is unavailable, falls back to a PNG sequence
in <output>_pngs/ which can be assembled with ffmpeg manually.
"""
from __future__ import annotations
import sys, os, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim


def render(frames_path: str, out_path: str | None = None, fps: int = 12):
    frames_path = Path(frames_path)
    with open(frames_path) as f:
        data = json.load(f)
    frames = data["frames"]
    if not frames:
        print(f"No frames in {frames_path}")
        return

    if out_path is None:
        out_path = str(frames_path.with_suffix("")) + ".mp4"
    out_path = Path(out_path)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.patch.set_facecolor("#0d0d0d")
    for ax in axes:
        ax.set_facecolor("#0d0d0d")
        ax.tick_params(colors="#aaaaaa")
        for sp in ax.spines.values(): sp.set_edgecolor("#333333")

    phi0 = np.array(frames[0]["phi_slice"])
    n0 = np.array(frames[0]["n_slice"])

    # Pre-scan to set color limits
    phi_max = max(abs(np.array(f["phi_slice"])).max() for f in frames)
    n_max = max(abs(np.array(f["n_slice"])).max() for f in frames)

    im0 = axes[0].imshow(phi0, origin="lower", cmap="RdBu_r",
                         vmin=-phi_max, vmax=phi_max)
    axes[0].set_title("phi (potential)", color="white")
    plt.colorbar(im0, ax=axes[0])
    im1 = axes[1].imshow(n0, origin="lower", cmap="plasma",
                         vmin=-n_max, vmax=n_max)
    axes[1].set_title("n (density perturbation)", color="white")
    plt.colorbar(im1, ax=axes[1])

    title = fig.suptitle("", color="white", fontsize=12)

    def update(idx):
        fr = frames[idx]
        im0.set_data(np.array(fr["phi_slice"]))
        im1.set_data(np.array(fr["n_slice"]))
        title.set_text(
            f"step {fr['step']}  |  E={fr['E']:.2e}  "
            f"Ez/Et={fr['E_zonal']/(fr['E_turb']+1e-12):.3f}  "
            f"acc={fr['acc']:.2e}  inj={fr['inj']:.3f}"
        )
        return [im0, im1, title]

    ani = anim.FuncAnimation(fig, update, frames=len(frames),
                             interval=1000 // fps, blit=False)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        ani.save(str(out_path), fps=fps, dpi=120,
                 savefig_kwargs={"facecolor": fig.get_facecolor()})
        print(f"Wrote {out_path}")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"ffmpeg unavailable ({e}). Writing PNG sequence instead.")
        pngs_dir = out_path.with_suffix("")
        pngs_dir = Path(str(pngs_dir) + "_pngs")
        pngs_dir.mkdir(parents=True, exist_ok=True)
        for i, fr in enumerate(frames):
            update(i)
            fig.savefig(pngs_dir / f"frame_{i:05d}.png",
                        dpi=120, facecolor=fig.get_facecolor())
        print(f"PNG sequence in {pngs_dir}")
        print(f"Assemble with: ffmpeg -r {fps} -i {pngs_dir}/frame_%05d.png -c:v libx264 -pix_fmt yuv420p {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: render_frames.py <frames.json> [output.mp4]")
        sys.exit(1)
    out = sys.argv[2] if len(sys.argv) > 2 else None
    render(sys.argv[1], out)
