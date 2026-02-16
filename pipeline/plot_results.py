import csv
from pathlib import Path
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[1]
DB = REPO / "results" / "database.csv"
OUTDIR = REPO / "results" / "plots"

def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(DB.open()))
    if not rows:
        print("No data in database.csv yet.")
        return

    def col(name):
        return [float(r[name]) for r in rows]

    obj = col("objective")
    L = col("tip_length_mm")
    R = col("tip_radius_mm")
    t = col("wall_thickness_mm")
    d = col("inner_depth_mm")

    # Scatter: objective vs radius
    plt.figure()
    plt.scatter(R, obj)
    plt.xlabel("tip_radius_mm")
    plt.ylabel("objective")
    plt.title("Objective vs Tip Radius")
    plt.savefig(OUTDIR / "objective_vs_radius.png", dpi=200)

    # Scatter: objective vs thickness
    plt.figure()
    plt.scatter(t, obj)
    plt.xlabel("wall_thickness_mm")
    plt.ylabel("objective")
    plt.title("Objective vs Wall Thickness")
    plt.savefig(OUTDIR / "objective_vs_thickness.png", dpi=200)

    # Scatter: objective vs (length)
    plt.figure()
    plt.scatter(L, obj)
    plt.xlabel("tip_length_mm")
    plt.ylabel("objective")
    plt.title("Objective vs Tip Length")
    plt.savefig(OUTDIR / "objective_vs_length.png", dpi=200)

    # Scatter: objective vs inner_depth
    plt.figure()
    plt.scatter(d, obj)
    plt.xlabel("inner_depth_mm")
    plt.ylabel("objective")
    plt.title("Objective vs Inner Depth")
    plt.savefig(OUTDIR / "objective_vs_inner_depth.png", dpi=200)

    print("Saved plots to:", OUTDIR)

if __name__ == "__main__":
    main()
