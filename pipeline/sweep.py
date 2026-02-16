import json, itertools, random, copy, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUN_ONE = REPO / "pipeline" / "run_one.py"

def run(params: dict):
    tmp = REPO / "pipeline" / "_tmp_params.json"
    tmp.write_text(json.dumps(params, indent=2))
    subprocess.check_call(["python3", str(RUN_ONE), str(tmp)])

def main():
    base = json.loads((REPO / "pipeline" / "params_default.json").read_text())

    # Simple grid ranges (edit as you like)
    lengths = [8.0, 10.0, 12.0]
    radii   = [2.0, 3.0, 4.0]
    walls   = [0.2, 0.5, 0.8]
    depths  = [4.0, 6.0, 8.0]

    combos = list(itertools.product(lengths, radii, walls, depths))
    random.shuffle(combos)

    # Limit runs so you don't blow up compute time
    max_runs = 15
    for i, (L, R, t, d) in enumerate(combos[:max_runs], start=1):
        p = copy.deepcopy(base)
        p["tip_length_mm"] = L
        p["tip_radius_mm"] = R
        p["wall_thickness_mm"] = t
        p["inner_depth_mm"] = min(d, L)
        print(f"\n=== RUN {i}/{max_runs} ===  L={L} R={R} t={t} d={p['inner_depth_mm']}")
        run(p)

if __name__ == "__main__":
    main()
