import pandas as pd


def read_inegi_dataset(path):
    data =pd.read_csv(path, sep=(","))
    return data