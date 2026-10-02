"""Validate generated model data independently of the viewer."""
import json
from pathlib import Path
import struct
import numpy as np

root = Path(__file__).resolve().parents[1]
points = np.load(root / 'work/gaussians.npy')
manifest = json.loads((root / 'outputs/gaussian-manifest.json').read_text())
assert len(points) == manifest['count'] == 594640
assert len(points) == 2 * manifest['previous_count']
assert np.isfinite(points).all() and np.all(points[:, 9] > 0)
raw = (root / 'outputs/room-gaussians.ply').read_bytes()
header, payload = raw.split(b'end_header\n', 1)
assert len(payload) == len(points) * 17 * 4
assert f'element vertex {len(points)}' in header.decode()
ply = np.frombuffer(payload, dtype='<f4').reshape(-1, 17)
assert np.isfinite(ply).all()
assert np.allclose(np.linalg.norm(ply[:, 13:17], axis=1), 1, atol=1e-5)
glb = (root / 'outputs/room-clean.glb').read_bytes()
assert struct.unpack_from('<III', glb) == (0x46546c67, 2, len(glb))
scene = json.loads((root / 'work/scene.json').read_text())
allowed = {'Left wall', 'Right wall', 'Entry left wall', 'Kitchen side wall', 'Bathroom far wall'}
assert all(o['name'] in allowed for o in scene if o.get('autoCutaway'))
print('PASS: density, finite data, Gaussian PLY, rotations, GLB and cutaway scope')
