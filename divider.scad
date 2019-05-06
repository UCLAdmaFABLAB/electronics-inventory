inch = 1;
THICKNESS = 0.127 * inch;
KERF_H = 0.002 * inch;
KERF_V = 0.006 * inch;

WIDTH = 20* inch;
HEIGHT = 3 * inch;

module divider(width, height, segments = 8) {
  tab_height = height / 2;
  tab_width = THICKNESS;
  tab_height_sub = tab_height - KERF_V;
  tab_width_sub = tab_width - KERF_H;
  difference() {
    square([width, height]);
    for(i = [0 : segments]) {
      translate([i * (width - tab_width_sub) / segments, 0])
        square([tab_width_sub, tab_height_sub]);
    }
  }
}

divider(22 * inch, 1.5 * inch);
translate([0, 4, 0])
  divider(19 * inch, 1.5 * inch);
