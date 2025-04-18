import pandas as pd

def load_production_csv(file_path):
    """
    生産データCSVファイルを読み込む関数。
    必須列：['開始時刻', '終了時刻', '製品名', '生産数']
    """
    return pd.read_csv(file_path, parse_dates=['開始時刻', '終了時刻'])
