# PLUMBER
## Description
PLUMBER is a benchmark for developing sequence-based models for binding affinity prediction, based on the PLINDER benchmark. The test data points include the SMILES of a small ligand, the sequence of the monomeric target protein, and a binary activity label corresponding to Ki/Kd < 1 μM. PLINDER is employed to split the proteins into training and testing sets. To enhance flexibility, the training set includes continuous values and their corresponding signs (=, >, <) and is compiled from various sources: ChEMBL, BindingDB, and BioLip2.

`val.csv` and `test.csv` contain the following columns:

- `SMILES`: the SMILES representation of a molecule
- `sequence`: the amino acid sequence of a monomer target protein
- `uniprot_id`: the UniProt ID of that protein
- `source`: either chembl, bdb, or biolip
- `split`: always set to 'test'
- `is_active`: a binary label indicating if the molecule has a Ki/Kd < 1 μM

`train.csv` does not have an `is_active` column. Instead, it contains different columns useful for training. `ki`, `kd`, `ic50`, and `ec50` store activity values, while `ki_sign`, `kd_sign`, `ic50_sign`, and `ec50_sign` specify the corresponding relationship, such as =, <, or >. You can choose to use only Ki/Kd equality data, but alternative strategies can incorporate the other activity types as well.


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
Many thanks to the [PLINDER](https://www.plinder.sh/) authors for the groundbreaking work on the advanced molecular data splitting.

## Citation
Durairaj, Janani, Yusuf Adeshina, Zhonglin Cao, Xuejin Zhang, Vladas Oleinikovas, Thomas Duignan, Zachary McClure, Xavier Robin, Gabriel Studer, Daniel Kovtun, Emanuele Rossi, Guoqing Zhou, Srimukh Prasad Veccham, Clemens Isert, Yuxing Peng, Prabindh Sundareson, Mehmet Akdel, Gabriele Corso, Hannes Stärk, Gerardo Tauriello, Zachary Wayne Carpenter, Michael M. Bronstein, Emine Kucukbenli, Torsten Schwede, Luca Naef. 2024. “PLINDER: The Protein-Ligand Interactions Dataset and Evaluation Resource.”
[bioRxiv](https://doi.org/10.1101/2024.07.17.603955)
[ICML'24 ML4LMS](https://openreview.net/forum?id=7UvbaTrNbP)
