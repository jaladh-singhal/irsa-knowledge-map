# SPHEREx at IRSA

> Where SPHEREx data lives at the NASA/IPAC Infrared Science Archive (IRSA) and how to query it: release status, and each dataset's query names, paths, DOIs and tutorials. Generated from the [IRSA knowledge map](https://github.com/jaladh-singhal/irsa-knowledge-map) on 2026-10-22; its names and links are checked against IRSA's live services weekly. A name missing here is not confirmed, not proof it doesn't exist: check `Irsa.list_collections()` and `Irsa.list_catalogs()` in astroquery before concluding.

SPHEREx: NASA, launched 2025-03-12. IRSA's mission page: <https://irsa.ipac.caltech.edu/Missions/spherex.html>.

## IRSA services

Datasets below list how to reach them as `<service key> <name>`, e.g. `sia euclid_DpdMerBksMosaic`.

- `sia`: Simple Image Access v2 (`https://irsa.ipac.caltech.edu/SIA?COLLECTION={name}`; Python: astroquery Irsa.query_sia(collection=...); docs <https://irsa.ipac.caltech.edu/ibe/sia.html>)
- `ssa`: Simple Spectral Access (`https://irsa.ipac.caltech.edu/SSA?COLLECTION={name}`; Python: astroquery Irsa.query_ssa(collection=...); docs <https://irsa.ipac.caltech.edu/ibe/ssa.html>)
- `tap`: Table Access Protocol (`https://irsa.ipac.caltech.edu/TAP`; Python: astroquery Irsa.query_tap(...) or pyvo; docs <https://irsa.ipac.caltech.edu/docs/program_interface/TAP.html>)
- `scs`: Simple Cone Search (`https://irsa.ipac.caltech.edu/SCS?table={name}`; docs <https://irsa.ipac.caltech.edu/docs/vo_scs.html>)
- `cutout`: IBE cutouts (append ?center=RA,DEC&size=DEG to an on-prem file URL; docs <https://irsa.ipac.caltech.edu/ibe/cutouts.html>)
- `browse`: Browsable directories (docs <https://irsa.ipac.caltech.edu/ibe/>)
- `s3`: AWS S3 (Open Data) (docs <https://irsa.ipac.caltech.edu/cloud_access/>)
- `s3_browser`: S3 bucket browser (docs <https://irsa.ipac.caltech.edu/cloud_access/>)
- `hats`: HATS Parquet (docs <https://irsa.ipac.caltech.edu/docs/parquet_catalogs/>)
- `gui`: Mission Data Explorer / IRSA Viewer
- `script`: Bulk download scripts (wget/curl)
- `moc`: MOC coverage maps (Python: mocpy MOC.from_fits(url); docs <https://irsa.ipac.caltech.edu/data/MOC/>)

## Releases

| Release | Id | Kind | Status | Released | Overview |
| --- | --- | --- | --- | --- | --- |
| Quick Release 3 | `spherex.qr3` | release | available | 2026-09 | <https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_qr.html> |
| Quick Release 2 | `spherex.qr2` | release | available | 2025-10 | <https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_qr.html> |
| Quick Release 1 | `spherex.qr1` | release | retired | 2025-07 | <https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_qr.html> |
| Data Release 1 | `spherex.dr1` | release | planned |  |  |
| SPHEREx Target List of Ice Sources (SPLICES) | `spherex.splices` | ancillary | available |  | <https://irsa.ipac.caltech.edu/data/SPHEREx/SPLICES/> |
| Comet 3I/ATLAS observations | `spherex.3i-atlas` | target_view | available |  | <https://irsa.ipac.caltech.edu/data/SPHEREx/docs/comet3iatlas/index.html> |
| Lab spectral calibration package | `spherex.spectral-calibrations` | ancillary | available |  | <https://irsa.ipac.caltech.edu/data/SPHEREx/docs/spherex_spectral_calibrations.html> |

## Quick Release 3 (`spherex.qr3`, available)

- Use caution combining with QR2 (different calibration)
- More R7 weeks expected with DR1 (late fall 2026, per the Explanatory Supplement)
- Release roots: browse <https://irsa.ipac.caltech.edu/ibe/data/spherex/qr3/>; s3 `s3://nasa-irsa-spherex/qr3/`; s3_browser <https://nasa-irsa-spherex.s3.us-east-1.amazonaws.com/index.html>
- **Spectral Image MEFs (wide)** (`spherex.qr3.spectral-images`, image): sia `spherex_qr3`; tap `spherex.plane`; tap `spherex.artifact`; tap `spherex.observation`; tap `spherex.obscore`; cutout; browse <https://irsa.ipac.caltech.edu/ibe/data/spherex/qr3/>; s3 `s3://nasa-irsa-spherex/qr3/level2/`; moc <https://irsa.ipac.caltech.edu/data/MOC/spherex_qr.moc.fits>; gui `SPHEREx Data Explorer`; files `level2/{planning_period}/l2b-v{version}-{proc_date}/{detector}/level2_{obs_id}D{detector}_spx_l2b-v{version}-{proc_date}.fits`
- **Spectral Image MEFs (deep fields)** (`spherex.qr3.spectral-images-deep`, image): sia `spherex_qr3_deep`; moc <https://irsa.ipac.caltech.edu/data/MOC/spherex.deep_field.moc.fits>
- **Effective PSF (ePSF)** (`spherex.qr3.epsf`, calibration): browse <https://irsa.ipac.caltech.edu/ibe/data/spherex/qr3/>; s3 `s3://nasa-irsa-spherex/qr3/epsf/`; files `epsf/cal-epsf-v{version}-{proc_date}/{detector}/epsf_D{detector}_spx_cal-epsf-v{version}-{proc_date}.fits`
- **Calibration and ancillary products** (`spherex.qr3.calibration`, calibration): tap `spherex.provenance_input`; s3 `s3://nasa-irsa-spherex/qr3/`

## Quick Release 2 (`spherex.qr2`, available)

- Do not combine with QR1
- Use caution combining with QR3 (different calibration)
- Pipeline versions 6.4 to 6.5.6; see the PSF header known issue
- Release roots: browse <https://irsa.ipac.caltech.edu/ibe/data/spherex/qr2/>; s3 `s3://nasa-irsa-spherex/qr2/`; s3_browser <https://nasa-irsa-spherex.s3.us-east-1.amazonaws.com/index.html>
- **Spectral Image MEFs (wide)** (`spherex.qr2.spectral-images`, image): sia `spherex_qr2`; tap `spherex.plane`; tap `spherex.artifact`; tap `spherex.observation`; tap `spherex.obscore`; cutout; browse <https://irsa.ipac.caltech.edu/ibe/data/spherex/qr2/>; s3 `s3://nasa-irsa-spherex/qr2/level2/`; moc <https://irsa.ipac.caltech.edu/data/MOC/spherex_qr.moc.fits>; gui `SPHEREx Data Explorer`; files `level2/{planning_period}/l2b-v{version}-{proc_date}/{detector}/level2_{obs_id}D{detector}_spx_l2b-v{version}-{proc_date}.fits`
- **Spectral Image MEFs (deep fields)** (`spherex.qr2.spectral-images-deep`, image): sia `spherex_qr2_deep`; moc <https://irsa.ipac.caltech.edu/data/MOC/spherex.deep_field.moc.fits>
- **Calibration and ancillary products** (`spherex.qr2.calibration`, calibration): tap `spherex.provenance_input`; s3 `s3://nasa-irsa-spherex/qr2/`

## Quick Release 1 (`spherex.qr1`, retired)

- Do not combine with QR2

## Data Release 1 (`spherex.dr1`, planned)

- R7 reprocessing of Surveys 1 and 2 (Explanatory Supplement)

## SPHEREx Target List of Ice Sources (SPLICES) (`spherex.splices`, available)

- Pre-launch community target list; source_id = SPHEREx Reference Catalog ID
- **SPLICES v8.6** (`spherex.splices.target-list`, catalog): gui `Gator`; moc <https://irsa.ipac.caltech.edu/data/MOC/splices.moc.fits>; browse <https://irsa.ipac.caltech.edu/data/SPHEREx/SPLICES/>

## Comet 3I/ATLAS observations (`spherex.3i-atlas`, available)

- Extended source: do not use the Spectrophotometry Tool
- Visits in Aug and Dec 2025
- **3I/ATLAS observation list and images** (`spherex.3i-atlas.observations`, image): browse `obscore_3I_Atlas.vot`; script `3IATLASImages-{wget,curl}.sh`

## Lab spectral calibration package (`spherex.spectral-calibrations`, available)

- Detector coordinates are x-flipped for detectors 4 to 6
- Pipeline calibrations are described in the user guide, not here
- **Channel maps, response curves and band-center maps** (`spherex.spectral-calibrations.lab-calibrations`, calibration): browse <https://irsa.ipac.caltech.edu/data/SPHEREx/docs/spherex_spectral_calibrations.html>

## Tutorials

- [Introduction to SPHEREx Spectral Images](https://caltech-ipac.github.io/irsa-tutorials/spherex-intro/): uses `spherex.qr3.spectral-images`
- [Download a collection of SPHEREx Spectral Image cutouts as a multi-extension FITS file](https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/): uses `spherex.qr3.spectral-images`, `spherex.qr2.spectral-images`
- [Understanding and Extracting the ePSF Extension in a SPHEREx Cutout](https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/): uses `spherex.qr3.epsf`, `spherex.qr2.spectral-images`
- [SPHEREx Source Discovery Tool IRSA Demo](https://caltech-ipac.github.io/irsa-tutorials/spherex-source-discovery-tool-demo/): uses `spherex.qr2.spectral-images`
- [Understanding and Analyzing SPHEREx Mosaic Cubes](https://caltech-ipac.github.io/irsa-tutorials/spherex-mosaic/): uses no listed dataset

## Tools

- [SPHEREx Data Explorer](https://irsa.ipac.caltech.edu/applications/spherex): Spectral image search with MOC overlays and a deep-field toggle
- [Spectrophotometry Tool](https://irsa.ipac.caltech.edu/applications/spherex/tool-spectrophotometry): Forced-photometry spectrum at known positions (max 20 sources)
- [Mosaic Tool](https://irsa.ipac.caltech.edu/applications/spherex/tool-mosaic): Custom multi-wavelength mosaic cubes
- [Cutout service](https://irsa.ipac.caltech.edu/data/SPHEREx/docs/cutout_tool.html): Cutouts via Data Explorer, direct URL (center/size) or Python
- [Moving Object Search Tool (MOST)](https://irsa.ipac.caltech.edu/applications/MOST): Find SPHEREx images of moving objects

## Identifiers

- **Planning Period**: Survey plan, ~3.5 days (e.g. `2025W18_2B`)
- **Observation ID**: Planning period + large slew + small slew (e.g. `2025W18_2B_0001_1`)
- **Detector**: 1-6, one per band (e.g. `D3`)
- **Version**: Product version in paths and filenames (e.g. `l2b-v12`)
- **Processing Date**: Year and day of year of processing (e.g. `2025-164`)

## Docs

- [IRSA SPHEREx tutorials](https://caltech-ipac.github.io/irsa-tutorials/spherex/)
- [SPHEREx Explanatory Supplement](https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp_QR.pdf)
- [SPHEREx Archive User Guide](https://caltech-ipac.github.io/spherex-archive-documentation/)
- [SPHEREx Data Access](https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-access)

## Known issues

- PSF extension header plane ordering: 
