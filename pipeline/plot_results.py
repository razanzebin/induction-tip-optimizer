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
        return [float(r[name]) for r in rows if r.get(name) not in (None, "", "NA")]

    # Prefer new column
    obj = col("objective")
    if not obj:
        print("No 'objective' column found with numeric data.")
        return

    L = col("tip_length_mm")
    R = col("tip_radius_mm")
    t = col("wall_thickness_mm")
    d = col("inner_depth_mm")

    def save_scatter(x, y, xlabel, title, filename):
        plt.figure()
        plt.scatter(x, y)
        plt.xlabel(xlabel)
        plt.ylabel("objective")
        plt.title(title)
        plt.savefig(OUTDIR / filename, dpi=200)

    save_scatter(R, obj, "tip_radius_mm", "Objective vs Tip Radius", "objective_vs_radius.png")
    save_scatter(t, obj, "wall_thickness_mm", "Objective vs Wall Thickness", "objective_vs_thickness.png")
    save_scatter(L, obj, "tip_length_mm", "Objective vs Tip Length", "objective_vs_length.png")
    save_scatter(d, obj, "inner_depth_mm", "Objective vs Inner Depth", "objective_vs_inner_depth.png")

    print("Saved plots to:", OUTDIR)

if __name__ == "__main__":
    main()
