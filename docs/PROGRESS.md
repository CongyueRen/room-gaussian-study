# Progress snapshot — 2026-10-02

## Objective

Produce a navigable, decluttered representation of a small room, preserve the user's corrected layout, and explore Gaussian rendering without requiring additional photography or a training installation.

## Completed

1. Reconstructed a simplified room from seven original photos, then incorporated three additional entry/bathroom references.
2. Corrected the bathroom orientation and the sequence from kitchen through a shared thin wall to toilet, washbasin and bathtub. Kept the toilet bay shallower than the tub bay.
3. Made the wardrobe a flush rectangular unit occupying the complete wall recess, directly adjoining the bathroom door frame.
4. Reduced the small entrance niche; unified indoor floor materials; adjusted bedside storage, desk and chair spacing.
5. Limited automatic wall hiding to the two long exterior sides, keeping internal partitions fixed.
6. Built the first Gaussian surface version with 297,320 splats.
7. Doubled sampling to 594,640 splats, reducing individual tangent scales by sqrt(2). This adds fresh samples rather than duplicating old points.
8. Prepared English viewers, PLY/GLB exports, reusable source, documentation and this repository homepage.

## Data and provenance

- Source: hand-authored geometry based on photographs and user feedback.
- Units: metres; Y is up.
- Gaussian representation: anisotropic tangent splats with a thin normal axis, baked diffuse color and constant base opacity.
- No camera calibration, structure-from-motion solution or photometric training was performed.
- Reference photographs are intentionally excluded from the repository and release.

## Validation

The current density is recorded in [the manifest](validation/gaussian-manifest.json); density, numeric and file checks are recorded in [the validation snapshot](validation/gaussian-validation.json).

The JavaScript checks execute viewer initialization, viewpoint controls and wall filtering in a mock WebGL environment. They do **not** prove shader compilation or successful GPU rendering. Static previews were independently rendered and visually checked.

## Known limitations

- Dimensions and concealed structures are estimates, not measurements.
- The mesh is simplified; the Gaussian representation preserves those simplifications.
- Soft edges, grain and transparency artifacts can remain, especially at grazing angles.
- The custom viewer uses an orthographic camera, depth sorting and surface-normal culling; it is not a complete 3DGS training or editing application.
- Standard PLY does not carry the custom exterior-wall grouping. Imported PLY scenes therefore retain all walls unless edited separately.
- Real browser validation, mobile performance and third-party Gaussian viewer compatibility remain unverified.

## Suggested next steps

1. Validate the existing viewer on the user's browser and measure interaction speed at 594,640 splats.
2. Verify import in a Gaussian editor such as SuperSplat.
3. Improve sample distribution and rendering performance if visible artifacts or slowdowns remain.
4. If photographic realism becomes the objective, capture overlapping images/video and evaluate a registered-photo training workflow as a separate phase.
