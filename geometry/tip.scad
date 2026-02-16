// ================================
// Parametric Induction Heating Tip
// CLI overrides via: openscad -D name=value
// ================================

// Only set defaults if NOT provided via -D
tip_length     = is_undef(tip_length)     ? 10   : tip_length;      // mm
tip_radius     = is_undef(tip_radius)     ? 3    : tip_radius;      // mm
wall_thickness = is_undef(wall_thickness) ? 0.5  : wall_thickness;  // mm
inner_depth    = is_undef(inner_depth)    ? 8    : inner_depth;     // mm
fn_smooth      = is_undef(fn_smooth)      ? 100  : fn_smooth;

$fn = fn_smooth;

// Guardrails (use new vars so we don't overwrite inputs)
_inner_depth = min(inner_depth, tip_length);
_wall_thickness = min(wall_thickness, tip_radius*0.95);

// Hollow cone tip
difference() {
    cylinder(h = tip_length, r1 = tip_radius, r2 = 0);
    translate([0,0, tip_length - _inner_depth])
        cylinder(h = _inner_depth,
                 r1 = tip_radius - _wall_thickness,
                 r2 = 0);
}
