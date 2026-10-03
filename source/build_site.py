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
