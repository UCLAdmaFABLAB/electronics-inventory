import json
import re
import unicodedata
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from svglib.svglib import svg2rlg

with open('manifest.json', 'r') as f:
     manifest = json.loads(f.read())
     drawers = manifest['drawers']
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
        w = size["dims"][0] * inch
        h = size["dims"][1] * inch
        name = size["name"]
        if name == item["size"]:
            return (w, h)

def handle_multiple(item):
    for i in range(0, item["quantity"]):
        _item = item.copy()
        _item["title"] = "%s #%i" % (item["title"], i + 1)
        _item["quantity"] = 1
        generate_tile(_item)
    return

def generate_tile(item):
    image = item['image']
    title = item['title']

    if item['quantity'] > 1:
        handle_multiple(item)
        return

    drawing = svg2rlg('images/%s' % image)
    canvas_size = get_canvas_size(item)
    width, height = drawing.wrap(0, 0)

    c = canvas.Canvas('tiles/%s.pdf' % slugify(title), pagesize=canvas_size)
    c.setFont('Helvetica', 10)
    c.setFillColor('black')
    c.setStrokeColor('black')

    center = ( (canvas_size[0] - width) / 2, (canvas_size[1] - height) / 2 )
    drawing.drawOn(c, center[0], center[1])
    yOffset = height / 2 + 20 if height > 40 else 40
    titleY = center[1] - yOffset
    if titleY < 15:
        titleY = 15
    if 'subtitle' in item:
        tx = c.beginText()
        c.drawCentredString(canvas_size[0] / 2, titleY, item['subtitle'])
        titleY += 14
    c.setFont('Helvetica', 15)
    c.drawCentredString(canvas_size[0] / 2, titleY, title)
    c.save()

for item in inventory:
    generate_tile(item)
