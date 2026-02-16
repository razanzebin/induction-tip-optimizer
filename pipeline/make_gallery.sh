#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/results/gallery"
SCAD="$ROOT/geometry/tip.scad"
mkdir -p "$OUT"

# Common params (adjust anytime)
L=12
R=3
T=0.5
D=8
FN=120

declare -A names=(
  [0]="solid_cone"
  [1]="hollow_cone"
  [2]="rod"
  [3]="hemisphere_cap"
  [4]="half_ellipsoid"
  [5]="pill"
)

for sid in 0 1 2 3 4 5; do
  name="${names[$sid]}"
  out="$OUT/${sid}_${name}.stl"
  echo "Exporting $out"
  openscad -o "$out" \
    -D "shape_id=$sid" \
    -D "tip_length=$L" \
    -D "tip_radius=$R" \
    -D "wall_thickness=$T" \
    -D "inner_depth=$D" \
    -D "fn_smooth=$FN" \
    "$SCAD" >/dev/null
done

echo "DONE. Gallery in: $OUT"
ls -lh "$OUT"
