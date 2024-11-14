from typing import Optional

from chembl_structure_pipeline.standardizer import standardize_mol
from chembl_structure_pipeline.exclude_flag import exclude_flag
from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit import RDLogger
from rdkit.Chem.AllChem import MolSanitizeException

RDLogger.DisableLog("rdApp.*")


LARGEST_FRAGMENT_CHOOSER = rdMolStandardize.LargestFragmentChooser()


def standardize(smiles: str) -> Optional[str]:
    """Standardize a molecule and return its SMILES and a flag indicating whether the molecule is valid.
    This version has exception handling, which the original in mol-finder/data doesn't have. I didn't change the mol-finder/data
    since there are a lot of other functions that depend on it and I didn't want to break them.
    """
    try:
        mol = Chem.MolFromSmiles(smiles, sanitize=False)
    except TypeError:
        return None

    try:
        exclude = exclude_flag(mol, includeRDKitSanitization=False)
    except AttributeError:
        return None
        
    if exclude:
        return None

    try:
        # Standardize with ChEMBL data curation pipeline. During standardization, the molecule may be broken
        # Choose molecule with largest component
        mol = LARGEST_FRAGMENT_CHOOSER.choose(mol)
        # Standardize with ChEMBL data curation pipeline. During standardization, the molecule may be broken
        mol = standardize_mol(mol)
        smiles = Chem.MolToSmiles(mol)
    # except MolSanitizeException:
    except (RuntimeError, MolSanitizeException):
        return None

    # Check if molecule can be parsed by RDKit (in rare cases, the molecule may be broken during standardization)
    if Chem.MolFromSmiles(smiles) is None:
        return None

    return smiles
