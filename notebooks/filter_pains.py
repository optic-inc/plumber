from loguru import logger
import medchem as mc
import pandas as pd
import argparse
import multiprocessing as mp
from tqdm import tqdm
from functools import partial
import datamol as dm

from pathlib import Path


def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


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
    logger.info("Converting molecules into datamol format...")
    with mp.Pool(mp.cpu_count()) as pool:
        molecules = list(tqdm(pool.imap(dm.to_mol, data[column_name]), total=len(data[column_name])))
    logger.info("Done.")
    logger.info("Filtering PAINS...")

    BATCH_SIZE = 1000
    batches_of_molecules = list(chunks(molecules, BATCH_SIZE))
    
    # Filter PAINS function
    f = partial(
        mc.functional.alert_filter,
        alerts=["PAINS"],
        n_jobs=0,
        progress=False,
        return_idx=False
    )

    num_processes = min(len(batches_of_molecules), mp.cpu_count())
    is_good = []
    with mp.Pool(processes=num_processes) as pool:
        result_iter = pool.imap(f, batches_of_molecules)
        for result in tqdm(result_iter, total=len(batches_of_molecules), desc="Processing batches"):
            is_good.extend(result)

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