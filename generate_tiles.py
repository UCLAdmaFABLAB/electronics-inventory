import json
import re
import os
import unicodedata
import sys
from pyx import bbox, canvas, color, document, path, svgfile, style, text, trafo, unit

text.set(text.LatexRunner)
text.preamble(r'\usepackage{helvet}')
text.preamble(r'\renewcommand\familydefault{\sfdefault}')

CUT_LINE = True

with open('manifest.json', 'r') as f:
     manifest = json.loads(f.read())
     inventory = manifest['inventory']
     sizes = manifest['sizes']

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value

def get_canvas_size(item):
    canvas_size = None
    for size in sizes:
        w = size["dims"][0] * unit.t_inch
        h = size["dims"][1] * unit.t_inch
        name = size["name"]
        if name == item["size"]:
            return (w, h)

def handle_multiple(item):
    for i in range(0, item["quantity"]):
        _item = item.copy()
        _item["title"] = "%s \#%i" % (item["title"], i + 1)
        _item["quantity"] = 1
        generate_tile(_item)
    return

def setEtch(canvas):
    if hasattr(canvas, 'items'):
        for c in canvas.items:
            setEtch(c)
    else:
        canvas.strokestyles = [
            style.linewidth(0.001),
            color.rgb.blue
        ]
        canvas.fillstyles = [
            color.rgb.white
        ]

def generate_tile(item):
    image = item['image']
    title = item['title']

    if item['quantity'] > 1:
        handle_multiple(item)
        return

    #72dpi is illustrator default
    drawing = svgfile.svgfile(0, 0, 'images/%s' % image, parsed=True, resolution=72)
    setEtch(drawing.canvas)
    canvas_size = get_canvas_size(item)
    drawing_size = (drawing.bbox().width(), drawing.bbox().height())

    dir = 'tiles/%s' % item['type']
    if not os.path.exists(dir):
        os.makedirs(dir)
    c = canvas.canvas()

    center = ( (canvas_size[0] - drawing_size[0]) / 2, (canvas_size[1] - drawing_size[1]) / 2 )
    c.insert(drawing, [trafo.translate(center[0], center[1])])

    yMargin = (canvas_size[1] - drawing_size[1]) / 2
    yPos = yMargin - yMargin / 2
    baseline = text.parbox.middle
    textbox = '{\large %s}' % title
    if 'subtitle' in item:
        textbox += '\n\n'
        textbox += item['subtitle']

    if yPos < (unit.t_inch / 2):
        baseline = text.parbox.bottom

    c.text(canvas_size[0] / 2, yPos, textbox, [
            text.halign.boxcenter,
            text.halign.flushcenter,
            text.parbox(canvas_size[0] - .25 * unit.t_inch, baseline = baseline)
    ])

    #draw Cut line
    if CUT_LINE:
        c.stroke(
            path.rect(0, 0, canvas_size[0], canvas_size[1]),
            [ style.linewidth(0.001), color.rgb.red ]
        )

    p = document.page(c, bbox=bbox.bbox(0, 0, canvas_size[0], canvas_size[1]))
    d = document.document([p])
    d.writeSVGfile('%s/%s.svg' % (dir, slugify(title)))

for item in inventory:
    generate_tile(item)
