# PLUMBER
## Description
PLUMBER is a benchmark for developing sequence-based models for binding affinity prediction, based on the Plinder benchmark. The test data points include the SMILES of a small ligand, the sequence of the monomeric target protein, and a binary activity label corresponding to Ki/Kd < 1 μM. Plinder is employed to split the proteins into training and testing sets. To enhance flexibility, the training set includes continuous values and their corresponding signs (=, >, <) and is compiled from various sources: ChEMBL, BindingDB, and BioLip2.

## Plinder
To develop generalizable sequence/structure-based models, we aim to test our model on unseen proteins. Standard techniques, such as time-split and random split, often result in test sets containing many very similar proteins, which limits the ability to measure generalizability. The recent benchmark, Plinder, proposed a compound metric that accounts for different types of similarity and splits datasets based on this metric. We decided to use their protein split assignment. While it is not perfect (as we lack ligand split information), it should yield more challenging splits compared to standard techniques.


## Columns
`val.csv` and `test.csv` contain the following columns:

- `SMILES`: the SMILES representation of a molecule
- `sequence`: the amino acid sequence of a monomer target protein
- `uniprot_id`: the UniProt ID of that protein
- `source`: either chembl, bdb, or biolip
- `split`: always set to 'test'
- `is_active`: a binary label indicating if the molecule has a Ki/Kd < 1 μM

`train.csv` does not have an `is_active` column. Instead, it contains different columns useful for training. `ki`, `kd`, `ic50`, and `ec50` store activity values, while `ki_sign`, `kd_sign`, `ic50_sign`, and `ec50_sign` specify the corresponding relationship, such as =, <, or >. You can choose to use only Ki/Kd equality data, but alternative strategies can incorporate the other activity types as well.

## Preprocessing
To ensure high data quality, we performed extensive preprocessing steps:
- Selected only monomer data
- Standardized SMILES
- Cleaned SMILES
- Prioritized data from BindingDB
- Filtered out PAINS
- Binarized values
- Deduplicated test/validation values


## Source Code
The `notebooks` directory contains all source code necessary to reproduce the benchmark:
- `01_chembl.ipynb` – Preprocesses ChEMBL database.
- `02_bindingdb.ipynb` – Preprocesses BindingDB.
- `03_biolip.ipynb` – Preprocesses BioLip.
- `04_merge.ipynb` – Aggregates all data.
- `filter_pains.py` – A function to filter out molecules not passing PAINS filter (used as an intermediate step in `04_merge.ipynb`)
- `standardize.py` – Source code for the molecules standardization (used as an intermediate step in `04_merge.ipynb`)

Ones the dataset is prepared from the notebooks, it can be published with `publish_to_polaris.py` script.

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
Many thanks to the [Plinder](https://www.plinder.sh/) authors for the groundbreaking work on the advanced molecular data splitting.
