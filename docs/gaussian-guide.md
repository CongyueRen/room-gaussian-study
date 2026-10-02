# Room Gaussian Splat Prototype

This prototype converts the corrected, decluttered room model into **anisotropic 3D Gaussian primitives**. It is a surface-sampled conversion, not a model trained from the uploaded photographs. Its colors and detail come from the existing room geometry; conversion cannot recover missing photographic texture, reflections or lighting.

## Density revision

This version uses 594,640 Gaussians, exactly twice the previous 297,320. Each triangle receives twice as many fresh surface samples; points are not duplicated. Tangential Gaussian scales shrink by a factor of sqrt(2), preserving approximate coverage while improving sampling detail. The PLY and offline viewer both contain the denser data.

## Open the viewer

Open `gaussian-viewer.html` in a WebGL-capable browser. It works offline and needs no installation. Drag to orbit, scroll or pinch to zoom. Use **Splat size** to adjust the Gaussian footprint. Smaller values reveal the individual splats; larger values make surfaces appear more continuous.

Only the two long exterior sides respond to **Outer walls** controls. All interior partitions and doorways remain fixed. The mesh viewer is preserved at `room-viewer.html`.

The viewer projects each Gaussian's anisotropic covariance onto the screen, sorts primitives by centre depth, and alpha-blends their Gaussian footprints. It uses an orthographic camera and surface-normal culling for this model-derived scene. This lightweight viewer is not a full photo-training engine. Some grain, soft edges and transparency artifacts are expected, especially at grazing angles.

## Files

- `room-gaussians.ply`: binary Gaussian PLY with positions, DC spherical-harmonic colors, logit opacity, logarithmic scales and normalized wxyz rotations. This is not an ordinary point-cloud PLY.
- `gaussian-viewer.html`: standalone viewer with embedded Gaussian data and wall-group metadata.
- `gaussian-preview.png`: independent Gaussian-rendered preview of the same dataset.
- `gaussian-manifest.json`: data provenance and primitive count.

The PLY uses metres and Y up. It contains complete walls. Wall grouping and automatic cutaway are implemented in the supplied HTML and are not preserved by the standard PLY interchange format.

## Optional tools

No additional skill, resource pack or software is required for this prototype. For editing, [SuperSplat](https://github.com/playcanvas/supersplat) runs in the browser and supports [Gaussian PLY import](https://github.com/playcanvas/developer-site/blob/main/docs/user-manual/supersplat/editor/import-export.md). Compatibility is based on its documented format; an actual SuperSplat import has not been tested here.

A later photorealistic reconstruction would need a suitable overlapping photo/video capture and camera registration before training. [OpenSplat](https://github.com/WebODM/OpenSplat) supports Apple Metal and registered camera/point inputs; this prototype does not require installing or running it. No photos or models have been published or uploaded to an external service.

## Validation and limits

Numeric fields, file size, quaternion normalization, Gaussian scales, viewer script execution and exterior-only visibility are checked locally. The preview is independently rendered from the Gaussian dataset. Browser rendering cannot be verified in this environment because local-file URL access is blocked. The supplied interactive viewer should therefore be treated as an unverified browser build until opened on the user's device.
