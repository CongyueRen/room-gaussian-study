import json, math, pathlib, base64
import numpy as np

root=pathlib.Path('outputs');scene=json.loads(pathlib.Path('work/scene.json').read_text());rng=np.random.default_rng(42)
rows=[];groups=[];ply=[];spacing=.043;density_multiplier=2
for oid,ob in enumerate(scene):
 groups.append({k:ob[k] for k in ['name','group','bounds','autoCutaway','wallOwner'] if k in ob})
 if ob['group'] in ['ceiling','glass']:continue
 v=np.array(ob['v']).reshape(-1,3);norm=np.array(ob['n']).reshape(-1,3)
 for idx in np.array(ob['i']).reshape(-1,3):
  a,b,c=v[idx];area=np.linalg.norm(np.cross(b-a,c-a))/2
  if area<1e-9:continue
  count=density_multiplier*max(1,int(math.ceil(area/spacing**2)))
  r=np.column_stack([(np.arange(count)+.5)/count,(np.arange(count)*.61803398875+rng.random())%1]);rt=np.sqrt(r[:,0]);weights=np.stack([1-rt,rt*(1-r[:,1]),rt*r[:,1]],axis=1)
  p=weights@v[idx];n=weights@norm[idx];n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-9)
  light=np.array([-.424,.707,.566]);col=np.array(ob['c'])[None,:]*(.65+.35*np.maximum(0,n@light))[:,None]
  scale=min(.046/math.sqrt(density_multiplier),max(.008/math.sqrt(density_multiplier),math.sqrt(area/count)*1.05));s=np.full((count,1),scale);opacity=np.full((count,1),.88)
  rows.append(np.concatenate([p,n,col,s,opacity,np.full((count,1),oid)],axis=1))
arr=np.concatenate(rows).astype('<f4');N=len(arr)
# Standard Gaussian PLY: DC spherical harmonics, log scales, logit opacity,
# and a normalized wxyz quaternion rotating local Z onto the surface normal.
n=arr[:,3:6];q=np.column_stack([1+n[:,2],-n[:,1],n[:,0],np.zeros(N)])
bad=np.linalg.norm(q,axis=1)<1e-6;q[bad]=[0,1,0,0];q/=np.linalg.norm(q,axis=1,keepdims=True)
out=np.concatenate([arr[:,:3],n,(arr[:,6:9]-.5)/.28209479177387814,np.log(arr[:,10:11]/(1-arr[:,10:11])),np.log(np.column_stack([arr[:,9],arr[:,9],np.maximum(arr[:,9]*.12,.001)])),q],axis=1).astype('<f4')
props=['x','y','z','nx','ny','nz','f_dc_0','f_dc_1','f_dc_2','opacity','scale_0','scale_1','scale_2','rot_0','rot_1','rot_2','rot_3']
header='ply\nformat binary_little_endian 1.0\ncomment Mesh-derived Gaussian surface approximation; not photo-trained\nelement vertex '+str(N)+'\n'+''.join('property float '+p+'\n' for p in props)+'end_header\n'
(root/'room-gaussians.ply').write_bytes(header.encode()+out.tobytes())
template=pathlib.Path(__file__).with_name('gaussian-viewer.html').read_text()
template=template.replace('__DATA__',base64.b64encode(arr.tobytes()).decode()).replace('__GROUPS__',json.dumps(groups)).replace('__COUNT__',f'{N:,}')
(root/'gaussian-viewer.html').write_text(template)
np.save('work/gaussians.npy',arr)
(root/'gaussian-manifest.json').write_text(json.dumps({'type':'mesh-derived anisotropic Gaussian splats','photo_trained':False,'count':N,'previous_count':297320,'density_multiplier':density_multiplier,'units':'metres','up_axis':'Y','source':'corrected room model','fields':props,'covariance':'surface tangent isotropic, normal axis thin','color':'baked model material and directional shading','opacity':.88},indent=2))
assert np.isfinite(out).all() and np.max(np.abs(np.linalg.norm(q,axis=1)-1))<1e-5
print('Generated',N,'Gaussian splats; PLY size',len(header)+out.nbytes)
