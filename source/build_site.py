"""Assemble GitHub Pages without committing large generated models."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
site=root/'work/site';site.mkdir(parents=True,exist_ok=True)
for name in ['room-viewer.html','gaussian-viewer.html','room-clean.glb','room-gaussians.ply','gaussian-manifest.json']:
 shutil.copy2(root/'outputs'/name,site/name)
shutil.copytree(root/'docs/images',site/'images',dirs_exist_ok=True)
shutil.copy2(root/'source/site.html',site/'index.html')
(site/'.nojekyll').touch()
print('Pages bundle:',sum(p.stat().st_size for p in site.rglob('*') if p.is_file()),'bytes')

# Serve a small HTML shell and a compressed binary dataset online. Keep the
# standalone embedded-data HTML unchanged for offline releases.
import gzip, json
import numpy as np
arr=np.load(root/'work/gaussians.npy')
compressed=gzip.compress(arr.astype('<f4',copy=False).tobytes(),compresslevel=6,mtime=0)
(site/'gaussians.bin.gz').write_bytes(compressed)
scene=json.loads((root/'work/scene.json').read_text())
groups=[{k:o[k] for k in ['name','group','bounds','autoCutaway','wallOwner'] if k in o} for o in scene]
shell=(root/'source/gaussian-viewer.html').read_text()
start=shell.index("let encoded=");end=shell.index("const canvas=",start)
loader='''const groups=__GROUPS__;
const status=document.getElementById('status');
if(!('DecompressionStream' in window))throw Error('This browser needs gzip decompression support. Try a current browser or download the offline viewer.');
const response=await fetch('gaussians.bin.gz');
if(!response.ok)throw Error('Dataset download failed: '+response.status);
const reader=response.body.getReader(),chunks=[];let received=0;
while(true){const {done,value}=await reader.read();if(done)break;chunks.push(value);received+=value.length;status.textContent='Downloading Gaussian data: '+(received/1e6).toFixed(1)+' MB';}
status.textContent='Decoding 3,000,000 Gaussians…';
const packed=await new Blob(chunks).arrayBuffer();
const prefix=new Uint8Array(packed,0,2);
const decoded=prefix[0]===31&&prefix[1]===139?await new Response(new Blob([packed]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer():packed;
if(decoded.byteLength!==144000000)throw Error('Incomplete Gaussian dataset. Reload to try again.');
const data=new Float32Array(decoded),N=data.length/12;
'''
shell=shell[:start]+loader+shell[end:]
shell=shell.replace('<script>','<script>\n(async()=>{',1).replace('</script>',"})().catch(error=>{document.getElementById('status').textContent=error.message;console.error(error);});\n</script>",1)
shell=shell.replace('__GROUPS__',json.dumps(groups)).replace('__COUNT__',f'{len(arr):,}').replace('Offline / Local','Online / GitHub Pages')
(site/'gaussian-viewer.html').write_text(shell)
print('Online Gaussian download:',len(compressed),'bytes; HTML:',len(shell.encode()),'bytes')
