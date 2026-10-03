"""Assert the tub, adjoining walls, doorway and balcony are connected."""
import json
from pathlib import Path
s=json.loads(Path('work/scene.json').read_text())
def bounds(name):
 o=next(o for o in s if o['name']==name)
 return [[min(o['v'][k::3]) for k in range(3)],[max(o['v'][k::3]) for k in range(3)]]
def close(a,b):assert abs(a-b)<1e-7,(a,b)
tub=bounds('Bathtub base');rear=bounds('Bathroom end wall');short=bounds('Recess back wall')
close(tub[1][2],rear[0][2]);close(tub[0][0],short[1][0])
close(tub[1][2]-tub[0][2],short[1][2]-short[0][2])
close(short[1][2],rear[0][2]);close(short[0][2],tub[0][2])
pier=bounds('Bathroom doorway rear pier')
assert pier[1][2]>=short[0][2] and pier[1][0]>=short[0][0]
frames=[o for o in s if o['name']=='Bathroom door jamb']
frame=frames[-1];close(max(frame['v'][2::3]),pier[0][2])
assert not any(o['group'] in ['bathTileFar','bathTileTub'] for o in s)
assert bounds('Shower rail')[1][0]<tub[0][0]+.1
for o in s:
 if o['name']=='Balcony full-height side wall':close(max(o['v'][1::3]),2.56)
close(bounds('Balcony roof')[0][1],2.56)
print('PASS: flush tub, tiled adjoining walls, short-wall/door connection, balcony enclosure')
