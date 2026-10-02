# Photo-Based Room Reconstruction

## Current layout

The bathroom fittings have been turned clockwise by 90 degrees from the preceding version. Along the room's long axis, the sequence is **kitchen → thin shared wall → toilet → washbasin → bathtub**. The toilet bay is shallower than the bathtub bay.

The wardrobe fills the entire recessed wall space up to the bathroom door frame. It is a single regular rectangular volume with a flush front; there is no open recessed passage between the wardrobe and bathroom doorway. The entrance niche remains narrow. Indoor flooring uses the same oak palette and plank direction throughout. The enlarged bedside-table space and closer desk/armchair arrangement are retained.

## Viewer

Open **room-viewer.html** in a WebGL-capable browser. It works offline without external dependencies.

- Drag to orbit; scroll or pinch to zoom.
- **Overview**, **Top view**, **Reverse**, and **Entry / Bath** select useful viewpoints.
- **Outer walls: Auto** hides obstructing segments of the two long exterior sides only. Interior partitions, kitchen side partitions, bathroom doorway walls, wardrobe surround, entrance door and end walls remain visible.
- **Outer walls: Show** and **Outer walls: Hide** affect only those same exterior segments. Interior walls remain unchanged in every mode.
- Low wall footprints remain visible. Glass has a separate toggle. The ceiling is omitted for viewing from above.
- Keep **room-clean.glb** beside the HTML file for the download button to work.

## Deliverables

- `room-viewer.html`: self-contained interactive model viewer.
- `room-clean.glb`: complete geometry with named components, in metres, Y up.
- `room-preview.png`: overall preview.
- `bathroom-preview.png`: bathroom and entry detail.
- `room-model-package.zip`: all current deliverables, plus editable source and checks.

The GLB includes complete walls. Automatic visibility is a viewer feature; it does not transfer into other modelling applications. An English-content compatibility copy remains at the previous viewer path so an already-open tab can be refreshed.

## Accuracy and checks

This is a simplified geometric reconstruction from ten photographs and the user's layout corrections, not a measured survey. Main-room dimensions of roughly 3.2 × 4.5 m and a 2.56 m ceiling are assumptions. Hidden structures, exact dimensions and finishes remain approximate. Do not use it for construction measurements.

The scene geometry, clockwise fitting rotation, kitchen-to-bathroom ordering, and exterior-only wall controls are checked programmatically. Preview images are rendered independently from the same geometry. Browser execution could not be verified in this environment because access to local-file URLs is blocked.

## Editable source

The package's `source/` folder includes the geometry generator, viewer template, preview renderer and logic checks. From an extracted package directory, run `python3 source/rebuild.py` to rebuild the GLB and viewer. Preview rendering additionally requires NumPy and Pillow; Node.js can run the viewer logic checks. No source photos are bundled.

## Gaussian surface prototype

Open `gaussian-viewer.html` for the model-derived Gaussian version, or read `GAUSSIAN-README.md`. This is a surface conversion, not a photo-trained reconstruction.
