import pandas as pd

def load_initial_inventory(file_path):
    """
    初期在庫CSVを読み込む関数。
    カラム: ['製品名', '数量']
    """
    return pd.read_csv(file_path)