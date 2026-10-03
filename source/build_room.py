import json, math, struct, pathlib, random
O=pathlib.Path('outputs'); O.mkdir(exist_ok=True)
objects=[]
colors={'wall':'eae9e2','white':'f3f0e7','wood':'bca17b','darkwood':'766650','blue':'8faebb','linen':'c1b6b9','cream':'e9e3d2','metal':'a6acaa','glass':'b8d4da','green':'668576','black':'414747'}
def rgb(c):
 c=colors.get(c,c);return [int(c[i:i+2],16)/255 for i in (0,2,4)]
def mesh(name,v,n,idx,col,group='furniture'):
 objects.append(dict(name=name,v=v,n=n,i=idx,c=rgb(col),group=group))
def box(name,x,y,z,w,h,d,col,group='furniture'):
 v=[];n=[];idx=[]
 faces=[([1,0,0],[(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)]),([-1,0,0],[(-1,-1,1),(-1,1,1),(-1,1,-1),(-1,-1,-1)]),([0,1,0],[(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)]),([0,-1,0],[(-1,-1,1),(-1,-1,-1),(1,-1,-1),(1,-1,1)]),([0,0,1],[(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]),([0,0,-1],[(1,-1,-1),(-1,-1,-1),(-1,1,-1),(1,1,-1)])]
 for normal,vs in faces:
  off=len(v)//3
  for a,b,c in vs:v += [x+a*w/2,y+b*h/2,z+c*d/2];n+=normal
  idx += [off,off+1,off+2,off,off+2,off+3]
 mesh(name,v,n,idx,col,group)
def ellipsoid(name,x,y,z,rx,ry,rz,col,group='furniture'):
 v=[];n=[];idx=[];a=24;b=12
 for j in range(b+1):
  t=math.pi*j/b
  for k in range(a+1):
   p=math.tau*k/a;s=[math.sin(t)*math.cos(p),math.cos(t),math.sin(t)*math.sin(p)]
   v += [x+s[0]*rx,y+s[1]*ry,z+s[2]*rz];nn=[s[0]/rx,s[1]/ry,s[2]/rz];l=math.sqrt(sum(q*q for q in nn));n += [q/l for q in nn]
 for j in range(b):
  for k in range(a):
   q=j*(a+1)+k;idx += [q,q+a+1,q+1,q+1,q+a+1,q+a+2]
 mesh(name,v,n,idx,col,group)
random.seed(3)
# One continuous oak material and plank grid across all interior zones.
def oak_floor(name,x0,x1,z0,z1):
 box(name,(x0+x1)/2,-.075,(z0+z1)/2,x1-x0,.14,z1-z0,'wood','floor')
 for ix in range(math.floor(x0/.2),math.ceil(x1/.2)):
  left=max(x0,ix*.2);right=min(x1,(ix+1)*.2)
  for iz in range(math.floor(z0/.68)-1,math.ceil(z1/.68)+1):
   start=iz*.68+(ix%2)*.34;lo=max(z0,start);hi=min(z1,start+.68)
   if hi-lo>.006:box('Continuous oak plank',(left+right)/2,.004,(lo+hi)/2,right-left-.003,.016,hi-lo-.003,['c5b18e','c8b694','c2ac88','cbb99a'][(ix*7+iz*3)%4],'floor')
oak_floor('Main room slab',0,3.2,0,4.5)
oak_floor('Entry floor',0,1.06,4.5,7.4)
oak_floor('Kitchen floor',1.06,3.2,4.5,5.3)
box('Left wall',-.065,1.28,2.25,.13,2.56,4.5,'wall','wall')
box('Right wall',3.265,1.28,2.25,.13,2.56,4.5,'wall','wall')
for x in [.018,3.182]:box('Skirting',x,.055,2.25,.026,.11,4.5,'white','wall')
# Window wall and balcony: large fixed pane at the bed, door at right.
box('Window sill wall',1.08,.40,-.04,2.16,.8,.13,'wall','window')
box('Window header',1.6,2.43,-.04,3.2,.26,.13,'wall','window')
for x in [.05,2.17,3.14]:box('Window frame',x,1.57,0,.07,1.75,.1,'white','window')
for y in [.83,2.32]:box('Window rail',1.1,y,0,2.15,.065,.11,'white','window')
box('Fixed window glass',1.1,1.57,-.025,2.06,1.42,.015,'glass','glass')
box('Balcony door glass',2.66,1.22,-.025,.89,2.12,.016,'glass','glass')
for y in [.12,2.31]:box('Door rail',2.66,y,0,.95,.065,.1,'white','window')
box('Window sill',1.1,.79,.075,2.2,.055,.28,'white','window')
box('Balcony floor',1.6,-.07,-.66,3.2,.12,1.2,'c9c8bd','balcony')
box('Balcony parapet',1.6,.47,-1.2,3.2,.96,.07,'d1d5d0','balcony')
for x in [-.065,3.265]:box('Balcony full-height side wall',x,1.28,-.63,.13,2.56,1.26,'wall','balcony')
box('Balcony roof',1.60,2.625,-.63,3.46,.13,1.26,'wall','balcony')
for x in [.17,3.02]:
 for i in range(8):ellipsoid('Blue curtain folds',x+(i-3.5)*.041,1.29,.16,.033,1.14,.047,'blue','curtains')
# Bed head against left wall, long direction across room.
box('Bed frame',1.05,.20,1.04,2.05,.34,1.48,'darkwood')
box('Bed headboard',.055,.51,1.04,.10,.82,1.52,'darkwood')
box('Mattress',1.09,.47,1.04,2,.22,1.43,'blue')
box('Neatly made blue duvet',1.32,.604,1.04,1.47,.075,1.44,'blue')
# Rounded rectangular pillows: flat central faces with softened corners.
for z in [.69,1.36]:
 ellipsoid('Rectangular blue pillow',.34,.655,z,.25,.075,.29,'blue')
 ob=objects[-1]
 for k in range(0,len(ob['v']),3):
  unit=[(ob['v'][k]-.34)/.25,(ob['v'][k+1]-.655)/.075,(ob['v'][k+2]-z)/.29]
  shaped=[math.copysign(abs(t)**.32,t) for t in unit]
  ob['v'][k:k+3]=[.34+shaped[0]*.25,.655+shaped[1]*.075,z+shaped[2]*.29]
  normal=[math.copysign(abs(t)**5.25,t)/r for t,r in zip(shaped,[.25,.075,.29])]
  length=math.sqrt(sum(t*t for t in normal))
  ob['n'][k:k+3]=[t/length for t in normal]
box('Duvet fold',.68,.645,1.04,.17,.065,1.44,'blue')
# Desk along left wall.
box('Desk top',.36,.765,2.96,.70,.055,1.24,'white')
for x in [.08,.64]:
 for z in [2.41,3.51]:box('Desk leg',x,.36,z,.075,.72,.075,'wood')
box('Bedside pedestal',.35,.30,2.07,.50,.60,.46,'white')
box('Bedside drawer',.61,.40,2.07,.02,.22,.40,'cream')
def chair(name,x,z,angle):
 start=len(objects)
 for a in [-.25,.25]:
  for b in [-.24,.24]:box(name+' foot',a,.095,b,.045,.19,.045,'darkwood')
 ellipsoid(name+' seat',0,.34,0,.36,.13,.35,'cream')
 ellipsoid(name+' back',0,.58,.27,.36,.34,.13,'cream')
 for a in [-.30,.30]:ellipsoid(name+' arm',a,.51,0,.095,.20,.32,'cream')
 for ob in objects[start:]:
  for key in ['v','n']:
   for j in range(0,len(ob[key]),3):
    a,b=ob[key][j],ob[key][j+2];ob[key][j]=a*math.cos(angle)+b*math.sin(angle)+(x if key=='v' else 0);ob[key][j+2]=-a*math.sin(angle)+b*math.cos(angle)+(z if key=='v' else 0)
chair('Lounge chair',.50,4.01,-math.pi/2)
chair('Desk chair',1.19,2.99,math.pi/2)
# 3 x 4 cube shelf on right wall, long axis parallel to wall.
for z in [.56,.96,1.36,1.76]:box('Cube shelf vertical',2.99,.79,z,.39,1.52,.035,'wood')
for y in [.04,.42,.8,1.18,1.56]:box('Cube shelf horizontal',2.99,y,1.16,.39,.035,1.24,'wood')
box('Cube shelf back',3.18,.80,1.16,.015,1.52,1.24,'wood')
for row,col in [(0,0),(0,2),(1,1),(1,2),(2,0),(3,0),(3,1)]:
 z=.76+col*.4;y=.22+row*.38
 box('Fabric storage bin',2.97,y,z,.32,.30,.32,'cream');box('Bin handle',2.802,y+.055,z,.007,.035,.095,'darkwood')
# Kept decorative vase, pampas, wall art and wall shelves.
ellipsoid('Flower vase',2.98,1.72,.65,.09,.15,.09,'cream')
for i in range(5):
 x=2.98+(i-2)*.035;box('Pampas stem',x,1.98,.65,.009,.42,.009,'wood');ellipsoid('Pampas plume',x,2.12+(i%2)*.04,.65,.037,.20,.035,'cabb98')
box('Wall print',3.185,1.93,1.40,.02,.55,.4,'d4cbb2')
for z,w,y in [(2.50,.88,1.23),(3.32,.50,1.85)]:
 box('Floating shelf',3.07,y,z,.25,.04,w,'wood')
 ellipsoid('Plant pot',3.06,y+.10,z+.1,.067,.085,.067,'white');box('Plant stem',3.06,y+.24,z+.1,.009,.22,.009,'green')
 for k in [-1,0,1]:ellipsoid('Orchid bloom',3.06,y+.34+k*.04,z+.1+k*.046,.035,.028,.035,'white')
# Small table near kitchen, facing opposite wall to desk.
box('Small dining table',2.87,.76,3.86,.61,.05,.92,'white')
for x in [2.63,3.10]:
 for z in [3.46,4.24]:box('Dining table leg',x,.37,z,.035,.74,.035,'metal')
for z in [3.63,4.04]:
 box('Stool seat',2.84,.46,z,.34,.045,.32,'wood')
 for x in [2.72,2.96]:
  for zz in [z-.11,z+.11]:box('Stool leg',x,.22,zz,.025,.44,.025,'metal')
# Kitchen and bathroom share one 12 cm wall, with no intervening void.
box('Kitchen bathroom shared thin wall',2.37,1.28,5.30,1.78,2.56,.12,'wall','partition')
box('Kitchen side wall',3.265,1.28,4.88,.13,2.56,.76,'wall','wall')

box('Kitchen canopy',2.4,2.40,4.75,1.60,.28,1.05,'wall','partition')
box('Kitchen lower cupboard',2.03,.45,4.99,.70,.87,.57,'white')
box('Mini refrigerator',2.78,.44,4.99,.70,.85,.57,'white')
box('Kitchen worktop',2.42,.91,4.99,1.51,.045,.63,'metal')
box('Sink rim',2.06,.94,4.97,.49,.028,.39,'metal')
box('Sink basin',2.06,.955,4.97,.40,.011,.29,'606e70')
box('Tap upright',2.12,1.07,5.16,.028,.24,.028,'metal');box('Tap spout',2.12,1.18,5.08,.028,.027,.18,'metal')
for z in [4.84,5.10]:ellipsoid('Electric hob',2.80,.947,z,.12,.008,.105,'black')
for ix in range(10):
 for iy in range(4):box('Grey backsplash tile',1.73+ix*.145,1.02+iy*.15,5.226,.14,.145,.025,'b3bdbb')
for x in [2.03,2.78]:
 for y,h in [(1.84,.55),(2.23,.22)]:
  box('Kitchen upper cabinet',x,y,5.06,.73,h,.38,'white');box('Cabinet pull',x,y-h/2+.06,4.859,.18,.012,.014,'metal')
 box('Base cabinet handle',x,.77,4.694,.21,.015,.02,'metal')
for x in [1.72,3.12]:
 for i in range(5):
  xx=x+(i-2)*.028;ellipsoid('Alcove curtain',xx,1.37,4.44,.024,1.06,.031,'white','curtains')
  for y in [.5,.83,1.16,1.49,1.82,2.15]:ellipsoid('Curtain leaf motif',xx,y+(i%2)*.07,4.407,.013,.045,.003,'green','curtains')
box('Entry left wall',-.065,1.28,5.95,.13,2.56,2.90,'wall','wall')
# Wardrobe is followed by a SIDE bathroom doorway, then a shallow recess,
# then the separate apartment entrance at the end of the corridor.
# Flush wardrobe: a single regular cuboid inside a wall-lined recess.
box('Built in wardrobe',1.222,1.22,5.285,.276,2.34,1.43,'wood','entry')
for z in [4.9275,5.6425]:
 box('Wardrobe door',1.072,1.22,z,.024,2.30,.707,'b49260','entry')
 box('Wardrobe handle',1.04,1.20,z,.030,.18,.018,'metal','entry')
box('Kitchen wardrobe separating short wall',1.42,1.28,4.90,.12,2.56,.80,'wall','partition')
box('Wardrobe surround front jamb',1.27,1.28,4.535,.42,2.56,.07,'wall','partition')
box('Wardrobe surround rear jamb',1.27,1.28,6.02,.42,2.56,.035,'wall','partition')
box('Wardrobe surround header',1.27,2.48,5.285,.42,.16,1.43,'wall','partition')
box('Wardrobe surround plinth',1.27,.04,5.285,.42,.08,1.43,'wall','partition')
# Along the room's long axis: kitchen, thin wall, toilet, basin, tub.
# Toilet bay is shallower across the room than the tub bay.
oak_floor('Bathroom toilet basin floor',1.42,3.20,5.30,6.04)
oak_floor('Bathroom bathtub floor',1.06,3.20,6.04,7.40)
oak_floor('Wardrobe recessed footprint',1.06,1.42,5.30,6.04)
box('Bathroom far wall',3.265,1.28,6.35,.13,2.56,2.10,'wall','wall')
box('Bathroom end wall',2.20,1.28,7.46,2.12,2.56,.12,'wall','wall')
box('Bathroom doorway front pier',1.42,1.28,5.70,.12,2.56,.68,'wall','partition')
box('Bathroom doorway rear pier',1.18,1.28,6.87,.24,2.56,.18,'wall','partition')
box('Bathroom doorway lintel',1.12,2.36,6.41,.12,.40,.74,'wall','partition')
for z in [6.055,6.7625]:box('Bathroom door jamb',1.12,1.06,z,.15,2.12,.035,'white','doorframe')
box('Bathroom door head frame',1.12,2.12,6.40875,.15,.045,.7425,'white','doorframe')
box('Bathroom open door',1.54,1.05,6.085,.76,2.08,.035,'white','bathroom')
box('Bathroom door handle',1.82,1.02,6.05,.11,.025,.035,'metal','bathroom')
# Half-depth entrance niche: only 18 cm beyond the corridor wall plane.
oak_floor('Recess floor',1.06,1.24,6.97,7.40)
box('Recess return wall',1.18,1.28,6.97,.24,2.56,.06,'wall','partition')
box('Recess back wall',1.30,1.28,7.09,.12,2.56,.62,'wall','partition')
box('Recess cabinet',1.17,.45,7.21,.12,.9,.32,'white','entry')
for y in [.23,.66]:box('Recess drawer front',1.103,y,7.21,.014,.40,.29,'white','entry')
for x,w in [(.045,.09),(1.11,.39)]:box('Entrance side pier',x,1.28,7.46,w,2.56,.12,'wall','wall')
box('Entrance transom',.52,2.36,7.46,.87,.40,.12,'wall','wall')
box('Apartment entrance door',.52,1.075,7.43,.85,2.13,.045,'d2d1bf','entrydoor')
box('Entrance handle',.82,1.0,7.395,.13,.026,.04,'metal','entrydoor')
bathroom_fixture_start=len(objects)
ellipsoid('Toilet pedestal',1.52,.23,5.69,.19,.23,.23,'white','bathroom')
ellipsoid('Toilet bowl',1.52,.43,5.81,.23,.16,.34,'white','bathroom')
ellipsoid('Toilet inner bowl',1.52,.565,5.88,.14,.012,.19,'bbc1b9','bathroom')
ellipsoid('Toilet raised lid',1.52,.72,5.49,.23,.31,.045,'white','bathroom')
box('Flush plate',1.52,1.00,5.377,.24,.20,.02,'cream','bathroom')
ellipsoid('Bathroom basin',2.19,.83,5.65,.30,.13,.27,'white','bathroom')
ellipsoid('Bathroom basin inset',2.19,.936,5.69,.22,.009,.18,'c6d0cc','bathroom')
box('Basin drain pipe',2.19,.47,5.52,.07,.58,.07,'metal','bathroom')
box('Basin tap',2.19,1.00,5.44,.035,.18,.035,'metal','bathroom')
box('Basin tap spout',2.19,1.075,5.50,.03,.025,.16,'metal','bathroom')
box('Bathroom mirror cabinet',1.87,1.62,5.47,1.26,.76,.20,'white','bathroom')
box('Bathroom mirror surface',1.87,1.62,5.578,1.15,.64,.012,'9dacac','bathroom')
box('Bathroom mirror shelf',1.87,1.22,5.57,1.33,.045,.32,'white','bathroom')
# Clockwise quarter-turn in plan, placing toilet nearest the kitchen.
for ob in objects[bathroom_fixture_start:]:
 for key in ['v','n']:
  for j in range(0,len(ob[key]),3):
   x,z=ob[key][j],ob[key][j+2]
   ob[key][j]=3.20-(z-5.36) if key=='v' else -z
   ob[key][j+2]=5.36+(x-1.18) if key=='v' else x
# Tub is flush with the end wall and short return wall beside the door.
# Its 0.62 m short edge matches the return wall from z=6.78 to 7.40.
box('Bathtub base',2.28,.18,7.09,1.84,.22,.62,'white','bathroom')
for z in [6.815,7.365]:box('Bathtub side rim',2.28,.36,z,1.84,.36,.07,'white','bathroom')
for x in [1.395,3.165]:box('Bathtub end rim',x,.36,7.09,.07,.36,.48,'white','bathroom')
box('Bathtub interior',2.28,.296,7.09,1.70,.016,.48,'dce1da','bathroom')
box('Shower rail',1.397,1.55,7.09,.025,1.13,.03,'metal','bathroom')
ellipsoid('Shower head',1.48,2.04,7.09,.085,.045,.09,'metal','bathroom')
box('Shower curtain rod',2.28,2.20,6.78,1.84,.022,.022,'metal','bathroom')
for i in range(7):ellipsoid('Gathered shower curtain',2.96+i*.026,1.38,6.78,.02,.79,.028,'cream','bathroom')
# Tile only the two adjoining walls of the tub, never the toilet side.
for iy in range(7):
 for ix in range(9):box('Bathtub long wall tile',1.36+(ix+.5)*1.84/9,.15+iy*.23,7.387,1.84/9-.004,.225,.018,'e4e3d9','bathTileLong')
 for iz in range(3):box('Bathtub short wall tile',1.373,.15+iy*.23,6.78+(iz+.5)*.62/3,.018,.225,.62/3-.004,'e4e3d9','bathTileShort')
box('Shoe cabinet',.18,.40,5.05,.34,.8,.77,'wood','entry')
for y in [.21,.58]:box('Shoe drawer',.36,y,5.05,.02,.32,.71,'white','entry')
box('Mirror backing',.03,.97,4.26,.06,1.81,.49,'white','entry')
box('Mirror',.067,.97,4.26,.009,1.70,.39,'9facad','entry')
box('Entry rug',.57,.018,4.99,.56,.015,1.45,'cream','entry')
for z in [4.30,5.68]:box('Rug border',.57,.028,z,.54,.006,.02,'darkwood','entry')
ellipsoid('Ceiling light',1.6,2.49,2.1,.25,.065,.25,'white','ceiling')
# Every wall has a low footprint that remains when the upper wall is hidden.
wall_names={o['name']:o for o in objects if o['group'] in ['wall','partition']}
for name,o in list(wall_names.items()):
 v=o['v'];lo=[min(v[k::3]) for k in range(3)];hi=[max(v[k::3]) for k in range(3)];o['bounds']=[lo,hi];o['autoCutaway']=name in ['Left wall','Right wall','Entry left wall','Kitchen side wall','Bathroom far wall']
 if lo[1]<.15 and hi[1]>.3:box(name+' footprint',(lo[0]+hi[0])/2,.065,(lo[2]+hi[2])/2,hi[0]-lo[0],.13,hi[2]-lo[2],'wall','wallbase')
for o in objects:
 if o['group']=='bathTileLong':o['wallOwner']='Bathroom end wall'
 if o['group']=='bathTileShort':o['wallOwner']='Recess back wall'
 if o['name']=='Grey backsplash tile':o['wallOwner']='Kitchen bathroom shared thin wall'
 if o['group']=='entrydoor':o['bounds']=[[.075,0,7.39],[.965,2.15,7.47]]
# Export genuine geometry as a self-contained GLB, metres, Y up.
blob=bytearray();views=[];acc=[];meshes=[];nodes=[];materials=[]
def buffer(values,fmt,typ,count,ext=None):
 while len(blob)%4:blob.append(0)
 off=len(blob);blob.extend(struct.pack('<'+fmt*len(values),*values));views.append(dict(buffer=0,byteOffset=off,byteLength=len(blob)-off))
 a=dict(bufferView=len(views)-1,componentType=5126 if fmt=='f' else 5125,count=count,type=typ)
 if ext:a.update(ext)
 acc.append(a);return len(acc)-1
for ob in objects:
 v=ob['v'];mi=len(materials);materials.append(dict(name=ob['name'],pbrMetallicRoughness=dict(baseColorFactor=ob['c']+[1],metallicFactor=0,roughnessFactor=.85),doubleSided=True))
 p=buffer(v,'f','VEC3',len(v)//3,dict(min=[min(v[k::3]) for k in range(3)],max=[max(v[k::3]) for k in range(3)]));n=buffer(ob['n'],'f','VEC3',len(v)//3);i=buffer(ob['i'],'I','SCALAR',len(ob['i']))
 meshes.append(dict(name=ob['name'],primitives=[dict(attributes=dict(POSITION=p,NORMAL=n),indices=i,material=mi)]));nodes.append(dict(name=ob['name'],mesh=len(meshes)-1,extras=dict(category=ob['group'],wallOwner=ob.get('wallOwner',''),autoCutaway=ob.get('autoCutaway',False))))
g=dict(asset=dict(version='2.0',generator='Photo-informed room reconstruction v4',extras={'units':'metres','accuracy':'Estimated from ten photos and user layout corrections; not a measured survey.'}),scene=0,scenes=[dict(nodes=list(range(len(nodes))))],nodes=nodes,meshes=meshes,materials=materials,buffers=[dict(byteLength=len(blob))],bufferViews=views,accessors=acc)
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4);blob+=b'\0'*((-len(blob))%4)
(O/'room-clean.glb').write_bytes(struct.pack('<III',0x46546c67,2,12+8+len(j)+8+len(blob))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(blob),0x004e4942)+blob)
(pathlib.Path('work')/'scene.json').write_text(json.dumps(objects,separators=(',',':')))
print(len(objects),'objects; GLB', (O/'room-clean.glb').stat().st_size)
