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
PLUMBER is a benchmark for developing sequence-based models for binding affinity prediction, based on the PLINDER benchmark. The val and test data points include the SMILES of a small ligand, the sequence of the monomeric target protein, and a binary activity label corresponding to Ki/Kd < 1 μM. PLINDER is employed to split the proteins into training and testing sets. To enhance flexibility, the training set includes continuous values and their corresponding signs (=, >, <) and is compiled from various sources: BindingDB, ChEMBL, and BioLip2.

`val.csv` and `test.csv` contain the following columns:

- `SMILES`: the SMILES representation of a molecule
- `sequence`: the amino acid sequence of a monomer target protein
- `uniprot_id`: the UniProt ID of that protein
- `source`: either chembl, bdb, or biolip
- `split`: either 'train' or 'test
- `is_active`: a binary label indicating if the molecule has a Ki/Kd < 1 μM

`train.csv` does not have an `is_active` column. Instead, it contains different columns useful for training. `ki`, `kd`, `ic50`, and `ec50` store activity values, while `ki_sign`, `kd_sign`, `ic50_sign`, and `ec50_sign` specify the corresponding relationship, such as =, <, or >. You can choose to use only Ki/Kd equality data, but alternative strategies can incorporate the other activity types as well.
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
