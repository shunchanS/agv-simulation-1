import pandas as pd

def load_shipping_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, parse_dates=["出荷日時"])
    df = df.sort_values("出荷日時").reset_index(drop=True)
    return df