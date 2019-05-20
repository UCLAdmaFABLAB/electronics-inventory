import json

with open('_data/manifest.json', 'r') as f:
     manifest = json.loads(f.read())
     inventory = manifest['inventory']
     sizes = manifest['sizes']

num_items = 0
types = set()
missing = []
no_image = []
for item in inventory:
    num_items += item['quantity']
    types.add(item['type'])
    if 'expected' in item and item['expected'] != item['quantity']:
        missing.append(item)
    if 'image' not in item:
        no_image.append(item)

print('Found %d items in %d drawers.' % (num_items, len(types)))
print()
print('%d missing or extraneous items:' % len(missing))
print()
for item in missing:
    title = item['title']
    if 'subtitle' in item:
        title += ' -- %s' % item['subtitle']
    print(title + ':')
    print('expected: %d' % item['expected'])
    print('actual: %d' % item['quantity'])
    print()
print('%d without images:' % len(no_image))
for item in no_image:
    print(item)
    print()
