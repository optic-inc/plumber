# PLUMBER
## Description
PLUMBER is a benchmark for developing sequence-based models for binding affinity prediction, based on the PLINDER benchmark. The test data points include the SMILES of a small ligand, the sequence of the monomeric target protein, and a binary activity label corresponding to Ki/Kd < 1 μM. PLINDER is employed to split the proteins into training and testing sets. To enhance flexibility, the training set includes continuous values and their corresponding signs (=, >, <) and is compiled from various sources: ChEMBL, BindingDB, and BioLip2.

`val.csv` and `test.csv` contains the following columns:

- `SMILES`: the SMILES representation of a molecule
- `sequence`: the amino acid sequence of a monomer target protein
- `uniprot_id`: the UniProt ID of that protein
- `source`: either chembl, bdb, or biolip
- `split`: always set to 'test'
- `is_active`: a binary label indicating if the molecule has a Ki/Kd < 1 μM

`train.csv` does not have an `is_active` column. Instead, it contains different columns useful for training. `ki`, `kd`, `ic50`, and `ec50` store activity values, while `ki_sign`, `kd_sign`, `ic50_sign`, and `ec50_sign` specify the corresponding relationship, such as =, <, or >. You can choose to use only Ki/Kd equality data, but alternative strategies can incorporate the other activity types as well.


## Source Code
The notebooks directory contains all source code necessary to reproduce the benchmark:
- `01_chembl.ipynb` – Preprocesses ChEMBL database.
- `02_bindingdb.ipynb` – Preprocesses BindingDB.
- `03_biolip.ipynb` – Preprocesses BioLip.
- `04_merge.ipynb` – Aggregates all data.
- `filter_pains.py` – Stand-alone script to filter out PAINS from the dataset. Used as an intermediate step in `04_merge.ipynb`.
- `standardize.py` – Source code for the standardization pipeline.

## Installation
The source code is assumed to be running on a POSIX-like machine. Prepare the environment:
```
conda create -n plumber -y python=3.11
conda activate plumber
pip install -r requirements.txt
```

## Development
To add a package to the `requirements.txt` add it to `requriements.in` and run `pip-compile` to generate new `requirement.txt`.

# Acknowledgements
