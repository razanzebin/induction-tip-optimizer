// =====================================
// Multi-family Parametric Tip Generator
// =====================================
// Use CLI like:
// openscad -o out.stl -D shape_id=1 -D tip_length=12 -D tip_radius=3 -D wall_thickness=0.5 -D inner_depth=8 tip.scad
//
// shape_id:
// 0 = solid_cone
// 1 = hollow_cone
// 2 = rod (cylinder)
// 3 = hemisphere_cap (dome)
// 4 = half_ellipsoid (cap)
// 5 = pill (capsule)

// Defaults only if not provided via -D
shape_id       = is_undef(shape_id)       ? 1    : shape_id;
tip_length     = is_undef(tip_length)     ? 10   : tip_length;      // mm
tip_radius     = is_undef(tip_radius)     ? 3    : tip_radius;      // mm
wall_thickness = is_undef(wall_thickness) ? 0.5  : wall_thickness;  // mm
inner_depth    = is_undef(inner_depth)    ? 8    : inner_depth;     // mm
fn_smooth      = is_undef(fn_smooth)      ? 120  : fn_smooth;

$fn = fn_smooth;

// Guardrails
L = max(tip_length, 0.01);
R = max(tip_radius, 0.01);
t = min(max(wall_thickness, 0.0), 0.95*R);
d = min(max(inner_depth, 0.0), L);

// --- shape modules ---
module solid_cone() {
    cylinder(h=L, r1=R, r2=0);
}

module hollow_cone() {
    difference() {
        cylinder(h=L, r1=R, r2=0);
        translate([0,0, L-d])
            cylinder(h=d, r1=max(R-t, 0.0), r2=0);
    }
}

module rod() {
    cylinder(h=L, r=R);
}

module hemisphere_cap() {
    // Dome sitting on z=0 plane, height ~ R
    intersection() {
        sphere(r=R);
        translate([-2*R,-2*R,0]) cube([4*R,4*R,2*R], center=false);
    }
}

module half_ellipsoid() {
    // Ellipsoid cap: radii (R,R,alpha*R). Use alpha= L/R but limit it.
    alpha = min(max(L/R, 0.2), 4.0);
    intersection() {
        scale([1,1,alpha]) sphere(r=R);
        translate([-2*R,-2*R,0]) cube([4*R,4*R,4*R], center=false);
    }
}

module pill() {
    // Capsule of length L (end-to-end). Cylinder length is max(L-2R, 0).
    cylL = max(L - 2*R, 0);
    union() {
        translate([0,0,R]) cylinder(h=cylL, r=R);
        sphere(r=R);
        translate([0,0,R+cylL]) sphere(r=R);
    }
}

// --- select ---
if (shape_id == 0) solid_cone();
else if (shape_id == 1) hollow_cone();
else if (shape_id == 2) rod();
else if (shape_id == 3) hemisphere_cap();
else if (shape_id == 4) half_ellipsoid();
else if (shape_id == 5) pill();
else hollow_cone();
