# Project progress

## Current milestone: 3M-point public demo

The existing room has been reconstructed from ten phone photos with iterative user corrections. It is a decluttered geometric approximation, not a trained photographic reconstruction.

Completed: kitchen and bathroom layout; wardrobe recess and doorway; consistent indoor floor; bedside clearance; curtain-matched gray-blue bedding; two rectangular pillows; tub flush to connected walls; shower on its short wall; tiles confined to the two tub walls; full-height balcony sides and roof.

Gaussian sampling progressed from 297,320 to 594,640 to 1,189,280, then exactly 3,000,000 fresh surface samples. The viewer has an independent point-count slider and footprint slider. Count selection uses a deterministic uniform nested subset; a cached bucket depth sort avoids sorting again when only point count changes.

Delivery: English mesh and Gaussian viewers, GLB, Gaussian PLY, manifest, overview/top/reverse/bath renders, reproducible source, MIT license, and a GitHub Actions deployment for the public interactive demo.

## Verified scope

Data and connection assertions, mock-WebGL viewer logic, and independent static renders. These are not a real-browser GPU or performance benchmark. The photos remain private and are not present in the repository.

## Future work

Interior-style generation/training, movable furniture, furniture addition/removal, material and soft-furnishing alternatives, saved layout comparisons, and real-time editing. None of these planned editing/generation features is implemented yet.
