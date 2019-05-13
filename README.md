# DMA Fab Lab Electronics Inventory
### Inventory and layout for electronics cabinet.

### Overview

This repository contains metadata about the items in inventory in the lab, as well as a script `generate_tiles.py` used to generate the labels/placeholders for items in the electronics cabinet. `images` contains actual-size SVG footprint drawings for each item in inventory, while `manifest.json` contains a listing of all items along with quantity and sizing details.

### Generating Tiles

**Prerequisites:**
- Python 3
- TeX or compatible distribution

Start by installing Python and TeX if they are not already present on your machine. Procedures will vary based on OS, but the versions at [python.org](https://www.python.org/) and [tug.org](http://www.tug.org/begin.html#install) should work in most cases.

Use pip to install PyX from the requirements.txt file:

```
pip3 install -r requirements.txt
```

Now you can run the script. Depending on your environment you may need to use the executable `python3` instead.

```
python generate_tiles.py
```

This script accepts no command line arguments and inspects `manifest.json` to determine which tiles to output and where to find associated images. Tiles will be output as SVG inside a new `tiles` directory.


### Manifest

`manifest.json` is formatted in two sections:
- `"inventory"`
- `"sizes"`

**Inventory**

Inventory is an array of objects with the following keys:

```
"title": Short description of the item
"subtitle": [optional] Details about the item (platform, version, etc.)
"image": Path to an svg thumbnail. Relative to 'images' dir.
"size": Determines size of tile generated. Should be one of the `names` from sizes listing, below.
"type": Group/drawer to which the item pertains. Determines output dir.
"quantity": Number of this item on-hand. Each item will be output `quantity` times.
```

Each unique item should be listed. Identical objects should not be listed twice, instead indicate `quantity`.


**Sizes**

Sizes is a listing of the dimensions of permitted tile sizes, in inches. It is formatted as an array of objects where `name` is a memorable token and `dims` is an array of `[width, height]` in inches.

Currently supported sizes as of this writing:

```
{ "name": "tiny", "dims": [2.6, 2.2] },
{ "name": "small", "dims": [2.6, 4.6] },
{ "name": "medium", "dims": [5.35, 4.6] },
{ "name": "large", "dims": [2.6, 9.3 ] },
{ "name": "xlv", "dims": [5.35, 9.3] },
{ "name": "xlh", "dims": [8.05, 4.6] }
```
