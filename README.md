# PLUMBER
### Description
PLUMBER is a benchmark for developing sequence-based models for binding affinity prediction, based on the PLINDER benchmark. The test data points include the SMILES of a small ligand, the sequence of the monomeric target protein, and a binary activity label corresponding to Ki/Kd < 1 μM. PLINDER is employed to split the proteins into training and testing sets. To enhance flexibility, the training set includes continuous values and their corresponding signs (=, >, <) and is compiled from various sources: ChEMBL, BindingDB, and BioLip2.

The notebooks directory contains all source code necessary to reproduce the benchmark:
- `01_chembl.ipynb` – Preprocesses ChEMBL database.
- `02_biolip.ipynb` – Preprocesses BioLip.
- `03_bindingdb.ipynb` – Preprocesses BindingDB.
- `04_gather.ipynb` – Aggregates all data.
- `filter_pains.py` – Stand-alone script to filter out PAINS from the dataset. Used as an intermediate step in `04_gather.ipynb`.
- `standardize.py` – Source code for the standardization pipeline.

### Installation
```
conda create -n plumber -y python=3.11
conda activate plumber
pip install -r requirements.txt
```

### Development
To add a package to the `requirements.txt` add it to `requriements.in` and run `pip-compile` to generate new `requirement.txt`.