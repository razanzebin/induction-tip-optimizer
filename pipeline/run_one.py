import json, subprocess, time, csv, math
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUNS = REPO / "results" / "runs"
DB   = REPO / "results" / "database.csv"

def sh(cmd, cwd=None):
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd, cwd=cwd)

def write_csv_row(row: dict):
    DB.parent.mkdir(parents=True, exist_ok=True)
    exists = DB.exists()
    with DB.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            w.writeheader()
        w.writerow(row)

def surrogate_objective(p: dict) -> float:
    """
    Surrogate objective until EM + thermal are plugged in.
    Higher is "better" (proxy for coupling vs mass).
    """
    L  = float(p["tip_length_mm"])
    R  = float(p["tip_radius_mm"])
    t  = float(p["wall_thickness_mm"])
    d  = float(p["inner_depth_mm"])

    outer_vol = (1/3) * math.pi * (R**2) * L
    inner_R = max(R - t, 0.0)
    inner_vol = (1/3) * math.pi * (inner_R**2) * min(d, L)

    mass_proxy = max(outer_vol - inner_vol, 1e-9)
    coupling_proxy = (R * L)
    hollowness = inner_vol / max(outer_vol, 1e-9)

    thin_penalty = 0.0
    if t < 0.2:
        thin_penalty = (0.2 - t) * 50.0

    score = (coupling_proxy * (1.0 + 0.8*hollowness)) - 0.6*mass_proxy - thin_penalty
    return float(score)

def main(params_path: str):
    params_path = Path(params_path)
    p = json.loads(params_path.read_text())

    run_id = time.strftime("run_%Y%m%d_%H%M%S")
    outdir = RUNS / run_id
    outdir.mkdir(parents=True, exist_ok=True)

    (outdir / "params.json").write_text(json.dumps(p, indent=2))

    stl_path = outdir / "tip.stl"
    scad = REPO / "geometry" / "tip.scad"
    fn_smooth = p.get("mesh_quality", {}).get("stl_fn", 100)

    sh([
        "openscad",
        "-o", str(stl_path),
        "-D", f"tip_length={p['tip_length_mm']}",
        "-D", f"tip_radius={p['tip_radius_mm']}",
        "-D", f"wall_thickness={p['wall_thickness_mm']}",
        "-D", f"inner_depth={p['inner_depth_mm']}",
        "-D", f"fn_smooth={fn_smooth}",
        str(scad)
    ])

    obj = surrogate_objective(p)

    metrics = {
        "status": "ok",
        "stl_bytes": stl_path.stat().st_size,
        "coil_frequency_khz": p.get("coil_frequency_khz"),
        "coil_current_A": p.get("coil_current_A"),
        "objective": obj,
        "objective_type": "surrogate_v1"
    }
    (outdir / "metrics.json").write_text(json.dumps(metrics, indent=2))

    row = {
        "run_id": run_id,
        "shape_family": p.get("shape_family"),
        "tip_length_mm": p.get("tip_length_mm"),
        "tip_radius_mm": p.get("tip_radius_mm"),
        "wall_thickness_mm": p.get("wall_thickness_mm"),
        "inner_depth_mm": p.get("inner_depth_mm"),
        "coil_frequency_khz": p.get("coil_frequency_khz"),
        "coil_current_A": p.get("coil_current_A"),
        "objective": metrics["objective"],
        "objective_type": metrics["objective_type"],
        "stl_path": str(stl_path)
    }
    write_csv_row(row)

    print(f"\nDONE: {run_id}")
    print(f"STL:  {stl_path}")
    print(f"OBJ:  {obj:.6f} ({metrics['objective_type']})")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 pipeline/run_one.py pipeline/params_default.json")
        raise SystemExit(2)
    main(sys.argv[1])
