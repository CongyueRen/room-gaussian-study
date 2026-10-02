"""Rebuild mesh and Gaussian outputs from a clean checkout."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--previews', action='store_true', help='Also render the PNG previews')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    (root / 'work').mkdir(exist_ok=True)
    (root / 'outputs').mkdir(exist_ok=True)
    source = root / 'source'
    def run(name, *arguments):
        subprocess.run([sys.executable, str(source / name), *arguments], check=True)
    run('build_room.py')
    viewer = (source / 'viewer.html').read_text().replace('__SCENE__', (root / 'work/scene.json').read_text())
    (root / 'outputs/room-viewer.html').write_text(viewer)
    run('build_gaussians.py')
    run('validate_data.py')
    if args.previews:
        run('render_depth.py')
        run('render_depth.py', 'entry')
        run('render_gaussians.py')
    print('Complete: generated files are in outputs/')

if __name__ == '__main__':
    main()
