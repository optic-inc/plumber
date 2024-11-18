from pathlib import Path

import numpy as np
import numcodecs
import pandas as pd
from polaris.experimental._dataset_v2 import DatasetV2
import zarr


DATA_DIR = Path("data/plumber")

train = pd.read_csv(DATA_DIR / 'train.csv', low_memory=False)
train['is_active'] = np.nan
val = pd.read_csv(DATA_DIR / 'val.csv', low_memory=False)
test = pd.read_csv(DATA_DIR / 'test.csv', low_memory=False)

missed_columns = [
    'ki', 'kd', 'ic50', 'ec50', 'ki_sign', 'kd_sign', 'ic50_sign', 'ec50_sign',
]
for column in missed_columns:
    val[column] = np.nan
    test[column] = np.nan

val = val[train.columns]
test = test[train.columns]
data = pd.concat([train, val, test], ignore_index=True)

data['ki_sign'] = data['ki_sign'].fillna("")
data['ic50_sign'] = data['ic50_sign'].fillna("")
data['kd_sign'] = data['kd_sign'].fillna("")
data['ec50_sign'] = data['ec50_sign'].fillna("")

plumber_zarr = 'plumber.zarr'
n = len(data)

root = zarr.open(plumber_zarr, mode='w')
root.empty('smiles', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('ki', shape=n, dtype=np.float32)
root.empty('ic50', shape=n, dtype=np.float32)
root.empty('kd', shape=n, dtype=np.float32)
root.empty('ec50', shape=n, dtype=np.float32)
root.empty('sequence', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('ki_sign', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('ic50_sign', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('kd_sign', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('ec50_sign', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('uniprot_id', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('source', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('split', shape=n, dtype=object, object_codec=numcodecs.VLenUTF8())
root.empty('is_active', shape=n, dtype=np.float32)

for col in train.columns:
    root[col][:] = data[col].values

zarr.convenience.consolidate_metadata(plumber_zarr)

readme = """
# PLUMBER
## Overview
![PLUMBER preview](https://github.com/optic-inc/plumber/blob/dfc5424d065a4ba153e0074b85ba10348cddd8eb/assets/plumber_preview.png)
PLUMBER is a benchmark for developing sequence-based models for binding event prediction, based on the PLINDER benchmark. PLUMBER is compiled as protein-ligand pairs dataset from various sources (ChEMBL, BindingDB, and BioLip2) and employes aggressive filtering from each of the datasets followed by molecules standardization, PAINS filtering and deduplication. The val/test sets are additionally binarized for binding event classification at a threshold of `< 1 μM` on Ki/Kd to have unified benchmark to compare models on. PLINDER is employed to split the proteins into training and testing sets. To enhance flexibility, the training set includes continuous values and their corresponding signs (=, >, <).

Note: *PLUMBER* states for *Protein–Ligand Unseen Matching Benchmark for Evaluating Robustness*

## PLINDER
To develop generalizable sequence/structure-based models, we aim to test our model on unseen proteins. Standard techniques, such as time-split and random split, often result in test sets containing many very similar proteins, which limits the ability to measure generalizability. The recent benchmark, [PLINDER](https://www.plinder.sh/), proposed a compound metric that accounts for different types of similarity on system level and splits datasets based on this metric. We decided to use their protein split assignment. While it is not perfect (as we lack ligand split information), it should yield more challenging splits compared to standard techniques.

![EDA](https://github.com/optic-inc/plumber/blob/041ddb780ca9001448d5f9b373b66547443a768a/eda.png)


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

# Acknowledgements
Many thanks to the [PLINDER](https://www.plinder.sh/) authors for the groundbreaking work on the advanced molecular data splitting.

"""

plumber_license = "CC-BY-4.0" # Should be one of those: "CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-4.0", "CC-BY-NC-SA-4.0", "CC0-1.0", "MIT"

dataset = DatasetV2(
    zarr_root_path=plumber_zarr,
    name="plumber", 
    description="Binding affinity prediction benchmark for sequence-based models", 
    owner="optic",
    tags=["sequence", "binding affinity", "sbdd", "small molecules"],
    readme=readme,
    license=plumber_license,
    source="https://github.com/optic-inc/plumber",
)

dataset.upload_to_hub(access="public", owner="optic")
