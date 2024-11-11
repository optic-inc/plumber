from loguru import logger
import medchem as mc
import pandas as pd
import argparse

from pathlib import Path

def filter_pains(data: pd.DataFrame, column_name: str = "smiles") -> pd.DataFrame:
    """Filters out PAINS alerts. Works REALLY long time. ~10 hours for BindingDB.

    Args:
        data (pd.DataFrame): BindingDB dataset.
        column_name (str, optional): Name of the SMILES column. Defaults to "smiles".

    Returns:
        pd.DataFrame: Preprocessed BindingDB dataset.
    """
    data = data.copy()
    logger.info("Molecules before the PAINS elimination: {}", len(data))
    is_good = mc.functional.alert_filter(
        mols=data[column_name].tolist(),
        alerts=["PAINS"],
        n_jobs=-1,
        progress=True,
        return_idx=False,
    )
    data = data[is_good]
    logger.info("Molecules after the PAINS elimination: {}", len(data))
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter pains")

    # Add arguments
    parser.add_argument("input_path", type=Path, help="The path to the file with 'smiles' column.")
    parser.add_argument("output_path", type=Path, help="The path to the output file.")

    # Parse the arguments
    args = parser.parse_args()

    data = pd.read_csv(args.input_path)
    result = filter_pains(data)
    result.to_csv(args.output_path, index=False)