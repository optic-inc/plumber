# PLUMBER
## Overview
PLUMBER is a benchmark for developing sequence-based models for binding event prediction, based on the PLINDER benchmark. PLUMBER is compiled as protein-ligand pairs dataset from various sources (ChEMBL, BindingDB, and BioLip2) and employes aggressive filtering from each of the datasets followed by molecules standardization, PAINS filtering and deduplication. The val/test sets are additionally binarized for binding event classification at a threshold of `< 1 μM` on Ki/Kd to have unified benchmark to compare models on. PLINDER is employed to split the proteins into training and testing sets. To enhance flexibility, the training set includes continuous values and their corresponding signs (=, >, <).

Note: *PLUMBER* states for *Protein–Ligand Unseen Matching Benchmark for Evaluating Robustness*

## PLINDER
To develop generalizable sequence/structure-based models, we aim to test our model on unseen proteins. Standard techniques, such as time-split and random split, often result in test sets containing many very similar proteins, which limits the ability to measure generalizability. The recent benchmark, [PLINDER](https://www.plinder.sh/), proposed a compound metric that accounts for different types of similarity on system level and splits datasets based on this metric. We decided to use their protein split assignment. While it is not perfect (as we lack ligand split information), it should yield more challenging splits compared to standard techniques.


## Data description
`val.csv` and `test.csv` contain the following columns:

- `SMILES`: standardized SMILES representation of a molecule
- `sequence`: amino acid sequence of a monomer target protein
- `uniprot_id`: UniProt ID of that protein
- `source`: either "chembl", "bdb", or "biolip"
- `split`: always set to "test"
- `is_active`: a binary label indicating if the molecule has a Ki/Kd < 1 μM

`train.csv` does not have an `is_active` column. Instead, it contains different columns useful for training. `ki`, `kd`, `ic50`, and `ec50` store activity values, while `ki_sign`, `kd_sign`, `ic50_sign`, and `ec50_sign` specify the corresponding relationship, such as =, <, or >. You can choose to use only Ki/Kd equality data, but alternative strategies can incorporate the other activity types as well.

## Preprocessing
To ensure high data quality, we performed extensive preprocessing steps:
- Selected only monomer data
- Standardized SMILES with [ChEMBL structure pipeline](https://github.com/chembl/ChEMBL_Structure_Pipeline)
- Cleaned SMILES
- Prioritized data from BindingDB
- Filtered out molecules with PAINS filter
- Binarized and deduplicated values with inconsistency check for val/test sets


## Source Code
The `notebooks` directory contains all source code necessary to reproduce the benchmark:
- `01_chembl.ipynb` – preprocesses ChEMBL database
- `02_bindingdb.ipynb` – preprocesses BindingDB
- `03_biolip.ipynb` – preprocesses BioLip 2
- `04_merge.ipynb` – aggregates all data
- `filter_pains.py` – a function to filter out molecules not passing PAINS filter (used as an intermediate step in `04_merge.ipynb`)
- `standardize.py` – source code for the molecules standardization (used as an intermediate step in `04_merge.ipynb`)
- `publish_to_polaris.py` - script for publishing dataset to [Polaris](https://polarishub.io/) platform

## Installation
The source code is assumed to be running on a POSIX-like machine. Prepare the environment:
```
conda create -n plumber -y python=3.11
conda activate plumber
conda install -c conda-forge polaris=0.9.1  # run it first before installing other dependencies
pip install -r requirements.txt
```

## Development
To add a package to the `requirements.txt` add it to `requriements.in` and run `pip-compile` to generate new `requirement.txt`.

# Acknowledgements
Many thanks to the [PLINDER](https://www.plinder.sh/) authors for the groundbreaking work on the advanced molecular data splitting.
