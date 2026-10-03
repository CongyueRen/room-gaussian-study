# Gaussian viewer guide

This model-derived prototype samples the corrected room geometry into exactly **3,000,000 anisotropic Gaussians**. It is not trained from photographs.

Use the [live demo](https://congyueren.github.io/room-gaussian-study/) or open `gaussian-viewer.html` from the offline release. Drag to orbit; scroll or pinch to zoom. Overview, Top view, Entry / Bath and Reverse provide camera presets. Switch to Mesh view to compare geometry.

**Gaussian count** selects 5–100% of the model (150,000–3,000,000 points). **Splat size** independently changes footprints. Selected count differs from drawn count because wall and backface filtering remove hidden samples. Downloads always include the full dataset. The Gaussian page is approximately 192 MB before compression and decoding; the mesh-first homepage avoids loading it until requested.

Only the two long exterior wall sides respond to Auto / Show / Hide. Interior partitions, the doorway, bathroom tiled walls, balcony side walls and balcony roof remain fixed.

The viewer projects anisotropic covariance into screen space, sorts centres into depth buckets and alpha blends Gaussian footprints, with an orthographic camera and surface-normal culling. These approximations can cause soft edges and transparency artifacts. Increasing density does not produce missing photographic detail.

The binary PLY uses metres, Y up, DC spherical harmonics, log scales, logit opacity and normalized wxyz rotations. The custom viewer's wall metadata is not carried by standard PLY interchange. Third-party imports have not been verified.

Validation covers finite data, counts, rotation norms, file structure, layout connections and mock-WebGL controls. Real-device rendering/performance is a separate check, not established by those tests. Full photo-trained reconstruction would require suitable overlapping captures and registered cameras; no such training is performed here.
