# Euclid at IRSA

> Where Euclid data lives at the NASA/IPAC Infrared Science Archive (IRSA) and how to query it: release status, and each dataset's query names, paths, DOIs and tutorials. Generated from the [IRSA knowledge map](https://github.com/jaladh-singhal/irsa-knowledge-map) on 2026-10-22; its names and links are checked against IRSA's live services weekly. A name missing here is not confirmed, not proof it doesn't exist: check `Irsa.list_collections()` and `Irsa.list_catalogs()` in astroquery before concluding.

Euclid: ESA (NASA partner), launched 2023-07-01. IRSA's mission page: <https://irsa.ipac.caltech.edu/Missions/euclid.html>.

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
| Early Release Observations | `euclid.ero` | release | available | 2024-05-23 | <https://irsa.ipac.caltech.edu/data/Euclid/docs/overview_ero.html> |
| Quick Release 1 | `euclid.q1` | release | available | 2025-03-19 | <https://irsa.ipac.caltech.edu/data/Euclid/docs/overview_q1.html> |
| Quick Release 2 | `euclid.q2` | release | available | 2026-06-24 | <https://irsa.ipac.caltech.edu/data/Euclid/docs/overview_q2.html> |
| Data Release 1 | `euclid.dr1` | release | planned | 2026-10-21 (expected) |  |

## Early Release Observations (`euclid.ero`, available)

- Predates Q1 and is a separate set of targeted observations; superseded by Q1 and later releases
- **ERO image stacks** (`euclid.ero.stacks`, image): sia `euclid_ero`; browse <https://irsa.ipac.caltech.edu/data/Euclid/ERO/images/>; gui `euclid_ero`; moc <https://irsa.ipac.caltech.edu/data/MOC/euclid_ero.moc.fits>; files `{target}/Euclid-{VIS|NISP}-Stack-ERO-{target}.DR3.tar`
- **ERO source catalogues** (`euclid.ero.stack-catalogs`, catalog): browse <https://irsa.ipac.caltech.edu/data/Euclid/ERO/images/>; files `{target}/Euclid-{VIS|NISP}-Catalog-ERO-{target}.DR3.tar.gz`

## Quick Release 1 (`euclid.q1`, available)

- Fields: EDF-N, EDF-F, EDF-S, LDN1641 (LDN1641 has no EXT data)
- MD5 checksums are under checksums/ in the on-prem root
- Bulk download scripts are in the S3 bucket under q1/
- Release roots: browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/>; s3 `s3://nasa-irsa-euclid-q1/q1/`; s3_browser <https://nasa-irsa-euclid-q1.s3.us-east-1.amazonaws.com/index.html>
- **MER multiwavelength mosaics** (`euclid.q1.mer-mosaic`, image): sia `euclid_DpdMerBksMosaic`; cutout; browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/MER/>; s3 `s3://nasa-irsa-euclid-q1/q1/MER/`; gui `Euclid Data Explorer`; moc <https://irsa.ipac.caltech.edu/data/MOC/euclid_q1_coverage.moc.fits>; DOI [10.26131/IRSA601](https://doi.org/10.26131/IRSA601); files `MER/{tile}/{instrument_dir}/EUC_MER_BGSUB-MOSAIC-{filter}_TILE{tile}-*_{timestamp}_*.fits`
- **MER segmentation maps** (`euclid.q1.mer-segmentation`, image): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/MER_SEG/>; s3 `s3://nasa-irsa-euclid-q1/q1/MER_SEG/`; files `MER_SEG/{tile}/EUC_MER_FINAL-SEGMAP_TILE{tile}-*_{timestamp}_*.fits`
- **VIS calibrated quadrant frames** (`euclid.q1.vis-frames`, image): sia `euclid_DpdVisCalibratedQuadFrame`; browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/VIS/>; s3 `s3://nasa-irsa-euclid-q1/q1/VIS/`; DOI [10.26131/IRSA599](https://doi.org/10.26131/IRSA599); files `VIS/{obs_id}/EUC_VIS_*.fits`
- **NISP calibrated frames** (`euclid.q1.nir-frames`, image): sia `euclid_DpdNirCalibratedFrame`; browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/NIR/>; s3 `s3://nasa-irsa-euclid-q1/q1/NIR/`; DOI [10.26131/IRSA600](https://doi.org/10.26131/IRSA600); files `NIR/{obs_id}/EUC_NIR_*.fits`
- **Raw VIS and NISP frames** (`euclid.q1.raw-frames`, image): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/RAW/>; s3 `s3://nasa-irsa-euclid-q1/q1/RAW/`; DOI [10.26131/IRSA614](https://doi.org/10.26131/IRSA614); files `RAW/{obs_id}/EUC_LE1_{VIS|NISP}-{obs_id_padded}-1-D_{timestamp}*.fits`
- **VMPZ HEALPix masks and maps** (`euclid.q1.vmpz`, image): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/VMPZ/>; s3 `s3://nasa-irsa-euclid-q1/q1/VMPZ/`; DOI [10.26131/IRSA617](https://doi.org/10.26131/IRSA617); files `VMPZ/VMPZ_HEALPIX_{BIT_MASK|FOOTPRINT_MASK|COVERAGE_MASK|DEPTH_MAP|INFO_MAP}/{tile}/EUC_LE3_VMPZ-ID_*-{tile}_{timestamp}_*.fits`
- **SIR 1D combined spectra** (`euclid.q1.sir-spectra`, spectrum): ssa `euclid_DpdSirCombinedSpectra`; browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/SIR/>; s3 `s3://nasa-irsa-euclid-q1/q1/SIR/`; DOI [10.26131/IRSA616](https://doi.org/10.26131/IRSA616); files `SIR/{tile}/EUC_SIR_W-COMBSPEC_{tile}_{timestamp}.fits`
- **SIR calibrated 2D science frames** (`euclid.q1.sir-frames`, image): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/SIR/>; s3 `s3://nasa-irsa-euclid-q1/q1/SIR/`; DOI [10.26131/IRSA615](https://doi.org/10.26131/IRSA615); files `SIR/{obs_id}/EUC_SIR_W-SCIFRM_BKGSUB_{obs_id}_*.fits`
- **MER final catalog** (`euclid.q1.mer-catalog`, catalog): tap `euclid_q1_mer_catalogue`; scs `euclid_q1_mer_catalogue`; gui `Euclid Data Explorer`; moc <https://irsa.ipac.caltech.edu/data/MOC/euclid_q1_mer_catalogue.moc.fits>; DOI [10.26131/IRSA602](https://doi.org/10.26131/IRSA602)
- **MER morphology catalog** (`euclid.q1.mer-morphology`, catalog): tap `euclid_q1_mer_morphology`; DOI [10.26131/IRSA603](https://doi.org/10.26131/IRSA603)
- **MER cutouts catalog** (`euclid.q1.mer-cutouts`, catalog): tap `euclid_q1_mer_cutouts`; DOI [10.26131/IRSA619](https://doi.org/10.26131/IRSA619)
- **PHZ photo-z catalog** (`euclid.q1.phz-photo-z`, catalog): tap `euclid_q1_phz_photo_z`; DOI [10.26131/IRSA604](https://doi.org/10.26131/IRSA604)
- **PHZ classification catalog** (`euclid.q1.phz-classification`, catalog): tap `euclid_q1_phz_classification`; DOI [10.26131/IRSA622](https://doi.org/10.26131/IRSA622)
- **PHZ galaxy SED catalog** (`euclid.q1.phz-galaxy-sed`, catalog): tap `euclid_q1_phz_galaxy_sed`; DOI [10.26131/IRSA621](https://doi.org/10.26131/IRSA621)
- **PHZ star SED catalog** (`euclid.q1.phz-star-sed`, catalog): tap `euclid_q1_phz_star_sed`; DOI [10.26131/IRSA620](https://doi.org/10.26131/IRSA620)
- **PHZ star template catalog** (`euclid.q1.phz-star-template`, catalog): tap `euclid_q1_phz_star_template`; DOI [10.26131/IRSA625](https://doi.org/10.26131/IRSA625)
- **PHZ NIR physical parameters catalog** (`euclid.q1.phz-nir-physical-parameters`, catalog): tap `euclid_q1_phz_nir_physical_parameters`; DOI [10.26131/IRSA624](https://doi.org/10.26131/IRSA624)
- **PHZ QSO physical parameters catalog** (`euclid.q1.phz-qso-physical-parameters`, catalog): tap `euclid_q1_phz_qso_physical_parameters`; DOI [10.26131/IRSA623](https://doi.org/10.26131/IRSA623)
- **SPE redshift catalog - galaxy candidates** (`euclid.q1.spe-galaxy-candidates`, catalog): tap `euclid_q1_spectro_zcatalog_spe_galaxy_candidates`; DOI [10.26131/IRSA607](https://doi.org/10.26131/IRSA607)
- **SPE redshift catalog - QSO candidates** (`euclid.q1.spe-qso-candidates`, catalog): tap `euclid_q1_spectro_zcatalog_spe_qso_candidates`; DOI [10.26131/IRSA608](https://doi.org/10.26131/IRSA608)
- **SPE redshift catalog - star candidates** (`euclid.q1.spe-star-candidates`, catalog): tap `euclid_q1_spectro_zcatalog_spe_star_candidates`; DOI [10.26131/IRSA609](https://doi.org/10.26131/IRSA609)
- **SPE redshift catalog - classification** (`euclid.q1.spe-classification`, catalog): tap `euclid_q1_spectro_zcatalog_spe_classification`; DOI [10.26131/IRSA606](https://doi.org/10.26131/IRSA606)
- **SPE redshift catalog - quality** (`euclid.q1.spe-quality`, catalog): tap `euclid_q1_spectro_zcatalog_spe_quality`; DOI [10.26131/IRSA605](https://doi.org/10.26131/IRSA605)
- **SPE lines catalog - spectral lines** (`euclid.q1.spe-line-features`, catalog): tap `euclid_q1_spe_lines_line_features`; DOI [10.26131/IRSA610](https://doi.org/10.26131/IRSA610)
- **SPE lines catalog - continuum features** (`euclid.q1.spe-continuum-features`, catalog): tap `euclid_q1_spe_lines_continuum_features`; DOI [10.26131/IRSA611](https://doi.org/10.26131/IRSA611)
- **SPE lines catalog - atomic indices** (`euclid.q1.spe-atomic-indices`, catalog): tap `euclid_q1_spe_lines_atomic_indices`; DOI [10.26131/IRSA612](https://doi.org/10.26131/IRSA612)
- **SPE lines catalog - molecular indices** (`euclid.q1.spe-molecular-indices`, catalog): tap `euclid_q1_spe_lines_molecular_indices`; DOI [10.26131/IRSA613](https://doi.org/10.26131/IRSA613)
- **SPE models catalog - lines** (`euclid.q1.spe-lines-models`, catalog): tap `euclid_q1_spectro_model_catalog_spe_lines_catalog`; DOI [10.26131/IRSA626](https://doi.org/10.26131/IRSA626)
- **SPE star models catalog** (`euclid.q1.spe-star-models`, catalog): tap `euclid_q1_spectro_model_catalog_spe_star_models`; DOI [10.26131/IRSA627](https://doi.org/10.26131/IRSA627)
- **MER catalog FITS files** (`euclid.q1.mer-catalog-files`, catalog): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/catalogs/MER_FINAL_CATALOG/>; s3 `s3://nasa-irsa-euclid-q1/q1/catalogs/MER_FINAL_CATALOG/`; files `catalogs/MER_FINAL_CATALOG/{tile}/EUC_MER_FINAL-{CAT|CUTOUTS-CAT|MORPH-CAT}_TILE{tile}-*_{timestamp}_*.fits`
- **PHZ catalog FITS files** (`euclid.q1.phz-catalog-files`, catalog): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/catalogs/PHZ_PF_OUTPUT_CATALOG/>; s3 `s3://nasa-irsa-euclid-q1/q1/catalogs/PHZ_PF_OUTPUT_CATALOG/`; browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/catalogs/PHZ_PF_OUTPUT_FOR_L3/>; s3 `s3://nasa-irsa-euclid-q1/q1/catalogs/PHZ_PF_OUTPUT_FOR_L3/`; files `catalogs/{PHZ_PF_OUTPUT_CATALOG|PHZ_PF_OUTPUT_FOR_L3}/{tile}/EUC_PHZ_*_{timestamp}_*.fits`
- **SPE catalog FITS files** (`euclid.q1.spe-catalog-files`, catalog): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/catalogs/SPE_PF_OUTPUT_CATALOG/>; s3 `s3://nasa-irsa-euclid-q1/q1/catalogs/SPE_PF_OUTPUT_CATALOG/`; files `catalogs/SPE_PF_OUTPUT_CATALOG/{tile}/EUC_SPE_WIDE-CAT-*-{tile}_*_{timestamp}_*.fits`
- **VIS calibrated-frame catalogs** (`euclid.q1.vis-frame-catalog`, catalog): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/catalogs/VIS_CAL_CATALOG/>; s3 `s3://nasa-irsa-euclid-q1/q1/catalogs/VIS_CAL_CATALOG/`; files `catalogs/VIS_CAL_CATALOG/{obs_id}/EUC_VIS_SWL-CAT-*.fits`
- **NISP calibrated-frame catalogs** (`euclid.q1.nir-frame-catalog`, catalog): browse <https://irsa.ipac.caltech.edu/ibe/data/euclid/q1/catalogs/NIR_CAL_CATALOG/>; s3 `s3://nasa-irsa-euclid-q1/q1/catalogs/NIR_CAL_CATALOG/`; files `catalogs/NIR_CAL_CATALOG/{obs_id}/EUC_NIR_W-CALIB-CAT_*.fits`
- **TILE ID to Observation ID association table** (`euclid.q1.tileid-association`, table): tap `euclid.tileid_association_q1`
- **Object ID to spectral file association table** (`euclid.q1.objectid-spectrafile-association`, table): tap `euclid.objectid_spectrafile_association_q1`
- **CAOM observation table** (`euclid.q1.caom-observation`, table): tap `euclid.observation_euclid_q1`
- **CAOM plane table** (`euclid.q1.caom-plane`, table): tap `euclid.plane_euclid_q1`
- **CAOM artifact table** (`euclid.q1.caom-artifact`, table): tap `euclid.artifact_euclid_q1`
- **Merged objects (HATS)** (`euclid.q1.merged-objects`, catalog): hats `s3://nasa-irsa-euclid-q1/contributed/q1/merged_objects/hats`; browse <https://irsa.ipac.caltech.edu/data/download/parquet/euclid/q1/merged_objects/hats/>

## Quick Release 2 (`euclid.q2`, available)

- VIS imaging only; no TAP catalogs or S3
- Uses the DR10 data model
- Calibration catalogues are not for statistics
- SHA-256 checksums: https://irsa.ipac.caltech.edu/data/Euclid/q2/checksums.sha256
- **VIS quadrant frames** (`euclid.q2.vis-frames`, image): sia `euclid_q2`; browse <https://irsa.ipac.caltech.edu/data/Euclid/q2/data/>; gui `euclid_q2`; moc <https://irsa.ipac.caltech.edu/data/MOC/euclid_q2.moc.fits>; files `EUC_VIS_SWL-{DET|BKG|WGT|CAT}-{obs_id}-{dither}-{expnum}__*.fits`
- **PSFEx PSF model** (`euclid.q2.psfex-model`, calibration): browse <https://irsa.ipac.caltech.edu/data/Euclid/q2/PSFEx_model/>
- **Calibration catalogues** (`euclid.q2.calibration-catalogues`, catalog): browse <https://irsa.ipac.caltech.edu/data/Euclid/q2/calibration_catalogues/>

## Data Release 1 (`euclid.dr1`, planned)

- No data released yet; only planned-coverage MOCs exist
- **Planned DR1 and survey coverage** (`euclid.dr1.planned-coverage`, table): moc <https://irsa.ipac.caltech.edu/data/MOC/euclid_dr1_wide.moc.moc.fits>; moc <https://irsa.ipac.caltech.edu/data/MOC/euclid_dr1_deep.moc.moc.fits>; moc <https://irsa.ipac.caltech.edu/data/MOC/euclid_planned_coverage.moc.fits>

## Tutorials

- [Euclid Q1: MER Mosaics](https://caltech-ipac.github.io/irsa-tutorials/euclid-intro-mer-images/): uses `euclid.q1.mer-mosaic`
- [Euclid Q1: MER Catalogs](https://caltech-ipac.github.io/irsa-tutorials/euclid-intro-mer-catalog/): uses `euclid.q1.mer-catalog`
- [Euclid Q1: SIR 1D Spectra](https://caltech-ipac.github.io/irsa-tutorials/euclid-intro-1d-spectra/): uses `euclid.q1.sir-spectra`
- [Euclid Q1: PHZ Catalogs](https://caltech-ipac.github.io/irsa-tutorials/euclid-intro-phz-catalog/): uses `euclid.q1.phz-photo-z`, `euclid.q1.mer-catalog`, `euclid.q1.mer-mosaic`, `euclid.q1.sir-spectra`
- [Euclid Q1: SPE Catalogs](https://caltech-ipac.github.io/irsa-tutorials/euclid-intro-spe-catalog/): uses `euclid.q1.spe-galaxy-candidates`, `euclid.q1.spe-line-features`, `euclid.q1.mer-catalog`
- [Euclid Q1 Merged Objects HATS Catalog: Introduction](https://caltech-ipac.github.io/irsa-tutorials/euclid-q1-hats-intro/): uses `euclid.q1.merged-objects`
- [Euclid Q1 Merged Objects HATS Catalog: Magnitudes](https://caltech-ipac.github.io/irsa-tutorials/euclid-q1-hats-magnitudes/): uses `euclid.q1.merged-objects`
- [HATS with LSDB](https://caltech-ipac.github.io/irsa-tutorials/irsa-hats-with-lsdb/): uses `euclid.q1.merged-objects`
- [Euclid Q1: Cloud Access](https://caltech-ipac.github.io/irsa-tutorials/euclid-cloud-access/): uses `euclid.q1.mer-mosaic`, `euclid.q1.sir-spectra`
- [Euclid Galaxy Clusters Analysis Tutorial](https://caltech-ipac.github.io/irsa-tutorials/euclid-clusters-tutorial/): uses `euclid.q1.mer-catalog`, `euclid.q1.phz-photo-z`
- [Exploring Star Clusters in the Euclid ERO Data](https://caltech-ipac.github.io/irsa-tutorials/euclid-ero/): uses `euclid.ero.stacks`

## Tools

- [Euclid Data Explorer](https://irsa.ipac.caltech.edu/applications/euclid): Search Q1 data by position, Tile ID or Object ID
- [Gator (Euclid)](https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-scan?projshort=Euclid): Catalog search
- [splitsci.py](https://irsa.ipac.caltech.edu/data/Euclid/q2/splitsci.py): Split Q2 DET files into SCI/FLG/RMS
- [integrity_check.sh](https://irsa.ipac.caltech.edu/data/Euclid/q2/integrity_check.sh): Verify Q2 downloads against checksums.sha256
- [EuclidExtractor](https://irsa.ipac.caltech.edu/data/Euclid/q2/EuclidExtractor/): Compute the Q2 PSFEx PSF model for chosen options (see Euclid_data_extraction.ipynb)

## Identifiers

- **TILE ID**: 9-digit MER tile; organizes MER products (e.g. `102018211`)
- **Observation ID**: Organizes Q1 VIS/NIR frame directories; zero-padded to 6 characters in Q2 filenames (e.g. 067070) (e.g. `2681`)
- **object_id**: Join key across MER, PHZ, SPE catalogs and the HATS merged objects
- **SIA obs_id**: Tile ID + instrument; tile ID can be derived from it (T05)

## Docs

- [IRSA Euclid tutorials](https://caltech-ipac.github.io/irsa-tutorials/euclid/)
- [Euclid Archive at IRSA User Guide](https://irsa.ipac.caltech.edu/data/Euclid/docs/euclid_archive_at_irsa_user_guide.pdf)
- [ESA Q1 Data Product Definitions](https://euclid.esac.esa.int/dr/q1/dpdd/)
- [Euclid Q2 paper](https://arxiv.org/abs/2606.25883)
- [Euclid Data Explorer known issues](https://irsa.ipac.caltech.edu/docs/known_issues/euclidbugslist.html)
