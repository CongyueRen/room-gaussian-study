import json, math, pathlib, sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
obs=json.loads(pathlib.Path('work/scene.json').read_text())
W,H=1500,1100
im=np.full((H,W,3),[232,232,224],dtype=np.uint8);depth=np.full((H,W),-1e8)
yaw=-.82;pitch=.85
entry='entry' in sys.argv
if entry:yaw=-.95;pitch=1.37
cy,sy,cp,sp=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch)
b=np.array([sy*cp,sp,cy*cp]);m=np.array([[cy,0,-sy],[-sy*sp,cp,-cy*sp],b]);target=np.array([1.55,.65,3.05] if not entry else [1.65,.70,6.0]);light=np.array([-.424,.707,.566])
targets=[[x,.65,z] for x in [.35,1.25,2.1,2.85] for z in [.6,1.4,2.4,3.5,4.2]]+[[.55,.65,z] for z in [4.8,5.65,6.35,7.12]]+[[x,.75,z] for x in [1.85,2.5,2.95] for z in [5.95,6.45,6.75]]+[[2.4,1.05,4.8],[1.17,.65,7.18],[2.84,.65,7.12]]
def hit(p,bounds):
 near=.035;far=40
 for k in range(3):
  if abs(b[k])<1e-7:
   if p[k]<bounds[0][k] or p[k]>bounds[1][k]:return False
  else:
   a,c=sorted([(bounds[0][k]-p[k])/b[k],(bounds[1][k]-p[k])/b[k]]);near=max(near,a);far=min(far,c)
   if near>far:return False
 return far>=near
hidden={o['name'] for o in obs if o.get('autoCutaway') and 'bounds' in o and any(hit(p,o['bounds']) for p in targets)}
for ob in obs:
 if ob['group'] in ['ceiling','glass'] or ob['name'] in hidden or ob.get('wallOwner') in hidden:continue
 if entry and (min(ob['v'][2::3])+max(ob['v'][2::3]))/2<4.35:continue
 vv=np.array(ob['v']).reshape(-1,3);norm=np.array(ob['n']).reshape(-1,3);p=(vv-target)@m.T;scale=115 if not entry else 223;p[:,0]=750+p[:,0]*scale;p[:,1]=600-p[:,1]*scale
 for inds in np.array(ob['i']).reshape(-1,3):
  a,bb,c=p[inds];ns=norm[inds];nn=ns.mean(axis=0)
  if nn@b<0:continue
  x0=max(0,math.floor(min(a[0],bb[0],c[0])));x1=min(W-1,math.ceil(max(a[0],bb[0],c[0])))
  y0=max(0,math.floor(min(a[1],bb[1],c[1])));y1=min(H-1,math.ceil(max(a[1],bb[1],c[1])))
  if x0>x1 or y0>y1:continue
  den=(bb[1]-c[1])*(a[0]-c[0])+(c[0]-bb[0])*(a[1]-c[1])
  if abs(den)<1e-8:continue
  yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
  aa=((bb[1]-c[1])*(xx-c[0])+(c[0]-bb[0])*(yy-c[1]))/den
  beta=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;gamma=1-aa-beta
  z=aa*a[2]+beta*bb[2]+gamma*c[2];dd=depth[y0:y1+1,x0:x1+1];mask=(aa>=-1e-7)&(beta>=-1e-7)&(gamma>=-1e-7)&(z>dd)
  shade=.60+.40*np.maximum(0,aa*(ns[0]@light)+beta*(ns[1]@light)+gamma*(ns[2]@light))
  cols=np.clip(shade[:,:,None]*np.array(ob['c'])*255,0,255).astype('uint8');im[y0:y1+1,x0:x1+1][mask]=cols[mask];dd[mask]=z[mask]
out=Image.fromarray(im);d=ImageDraw.Draw(out)
if entry:d.rectangle((0,0,1500,175),fill=(232,232,224))
def preview_font(size):
 for name in ['/System/Library/Fonts/Helvetica.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','DejaVuSans.ttf']:
  try:return ImageFont.truetype(name,size)
  except OSError:pass
 return ImageFont.load_default(size=size)
for txt,xy,size in [('PHOTO → SPACE / 04',(55,48),15),('Bathroom and Recessed Wardrobe' if entry else 'Room Reconstruction · Revised Bathroom',(55,87),32),('Based on 10 photos and layout corrections · Exterior-wall cutaway only',(55,136),16),('Estimated dimensions  |  Interior partitions remain visible at every angle',(55,1030),15)]:d.text(xy,txt,font=preview_font(size),fill='#304741')
out.save('outputs/bathroom-preview.png' if entry else 'outputs/room-preview.png')
print('Depth-rendered preview complete')
