inch = 1;
THICKNESS = 0.127 * inch;
KERF_H = 0.002 * inch;
KERF_V = 0.006 * inch;

WIDTH = 20* inch;
HEIGHT = 3 * inch;

TAB_HEIGHT = HEIGHT / 2;
TAB_WIDTH = THICKNESS;
TAB_HEIGHT_SUB = TAB_HEIGHT - KERF_V;
TAB_WIDTH_SUB = TAB_WIDTH - KERF_H;
COLUMNS = 8;
ROWS = 8;


difference() {
  square([WIDTH, HEIGHT]);
  for(i = [0 : ROWS]) {
    translate([i * (WIDTH - TAB_WIDTH_SUB) / ROWS, 0])
      square([TAB_WIDTH_SUB, TAB_HEIGHT_SUB]);
  }
}