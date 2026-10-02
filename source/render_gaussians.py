import json,math,pathlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
a=np.load('work/gaussians.npy');groups=json.loads(pathlib.Path('work/scene.json').read_text())
W,H=1400,1050;image=np.full((H,W,3),[.91,.91,.88],np.float32)
yaw=-.82;pitch=.85;cy,sy,cp,sp=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch)
r=np.array([cy,0,-sy]);u=np.array([-sy*sp,cp,-cy*sp]);b=np.array([sy*cp,sp,cy*cp]);target=np.array([1.55,.65,3.05]);pix=H/9.7
points=a[:,:3]-target;xy=np.column_stack([W/2+points@r*pix,H/2-points@u*pix]);depth=points@b
# Same exterior-only ray visibility as the interactive viewer.
samples=[[x,.65,z] for x in [.4,1.4,2.8] for z in [.7,2.5,4.2]]+[[x,.7,z] for x in [.55,2.6] for z in [5,6.3,7.1]]
def hit(p,bb):
 lo=.03;hi=40
 for k in range(3):
  if abs(b[k])<1e-7:
   if p[k]<bb[0][k] or p[k]>bb[1][k]:return False
  else:
   t0,t1=sorted([(bb[0][k]-p[k])/b[k],(bb[1][k]-p[k])/b[k]]);lo=max(lo,t0);hi=min(hi,t1)
   if lo>hi:return False
 return True
hidden={g['name'] for g in groups if g.get('autoCutaway') and any(hit(p,g['bounds']) for p in samples)}
visible=np.array([g['name'] not in hidden and g.get('wallOwner') not in hidden for g in groups])
for i in np.argsort(depth):
 p=a[i];n=p[3:6]
 if not visible[int(p[11])] or n@b<-.08:continue
 x,y=xy[i];s=p[9]*pix;nn=np.array([n@r,-n@u]);cov=s*s*(np.eye(2)-.9856*np.outer(nn,nn))+np.eye(2)*.3
 radius=math.ceil(3*math.sqrt(np.linalg.eigvalsh(cov)[1]));x0=max(0,int(x-radius));x1=min(W,int(x+radius)+1);y0=max(0,int(y-radius));y1=min(H,int(y+radius)+1)
 if x0>=x1 or y0>=y1:continue
 inv=np.linalg.inv(cov);yy,xx=np.mgrid[y0:y1,x0:x1];dx=xx+.5-x;dy=yy+.5-y;e=-.5*(inv[0,0]*dx*dx+2*inv[0,1]*dx*dy+inv[1,1]*dy*dy);alpha=np.where(e>=-4.5,p[10]*np.exp(e),0)[:,:,None]
 image[y0:y1,x0:x1]=image[y0:y1,x0:x1]*(1-alpha)+p[6:9]*alpha
out=Image.fromarray(np.clip(image*255,0,255).astype('uint8'));d=ImageDraw.Draw(out)
def preview_font(size):
 for name in ['/System/Library/Fonts/Helvetica.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','DejaVuSans.ttf']:
  try:return ImageFont.truetype(name,size)
  except OSError:pass
 return ImageFont.load_default(size=size)
for text,pos,size in [('GAUSSIAN SURFACE STUDY / 02 · HIGH DENSITY',(40,35),14),('Room · Gaussian Splat Preview',(40,70),29),('Model-derived anisotropic Gaussians · Not photo-trained',(40,115),15),(f'{len(a):,} Gaussians | Original furniture and corrected layout',(40,1005),14)]:d.text(pos,text,font=preview_font(size),fill='#304741')
out.save('outputs/gaussian-preview.png');print('Gaussian preview rendered')
