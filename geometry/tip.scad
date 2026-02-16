// ================================
// Parametric Induction Heating Tip
// ================================

// ---- Parameters ----
tip_length = 10;          // mm
tip_radius = 3;           // mm
wall_thickness = 0.5;     // mm
inner_depth = 8;          // mm

$fn = 100;  // smoothness

// ---- Geometry ----
difference() {
    // Outer cone
    cylinder(h = tip_length, r1 = tip_radius, r2 = 0);

    // Hollow cavity
    translate([0,0, tip_length - inner_depth])
        cylinder(h = inner_depth,
                 r1 = tip_radius - wall_thickness,
                 r2 = 0);
}
