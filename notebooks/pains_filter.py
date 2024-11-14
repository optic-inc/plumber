from functools import partial
from loguru import logger
import multiprocessing as mp

import datamol as dm
import medchem as mc
import pandas as pd
from tqdm import tqdm


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def filter_pains(data: pd.DataFrame, column_name: str = "smiles") -> pd.DataFrame:
    """Filter out molecules not passing the PAINS filter.

    Args:
        data: input dataset.
        column_name: name of the SMILES column. Defaults to "smiles".

    Returns:
        pd.DataFrame: filtered dataset.
    """
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

    data = data[is_good].reset_index(drop=True)
    logger.info("Molecules after the PAINS elimination: {}", len(data))

    return data
