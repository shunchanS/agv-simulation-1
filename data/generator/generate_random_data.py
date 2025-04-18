import pandas as pd
import random
from datetime import datetime, timedelta
import os

# 出力先ディレクトリ
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# 開始時刻
start_time = datetime(2025, 4, 14, 8, 0, 0)

# 製品リスト（10品番）
products = [f"P{i+1}" for i in range(10)]

# --- 生産データ生成 --- #
production_data = []
for i in range(1000):
    product = random.choice(products)
    qty = random.randint(10, 50)
    duration = random.randint(10, 60)  # 10〜60分で生産完了
    start = start_time + timedelta(minutes=i * 3)  # 3分おきに生産開始
    end = start + timedelta(minutes=duration)
    production_data.append([start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"), product, qty])

production_df = pd.DataFrame(production_data, columns=["開始時刻", "終了時刻", "製品名", "生産数"])
production_df.to_csv(os.path.join(output_dir, "production_test.csv"), index=False)

# --- 出荷データ生成 --- #
shipping_data = []
for i in range(1000):
    product = random.choice(products)
    qty = random.randint(5, 30)
    shipping_time = start_time + timedelta(minutes=i * 3 + random.randint(0, 5))  # 少しずらして出荷指示
    delivery_id = f"A{i+1:04d}"
    shipping_data.append([shipping_time.strftime("%Y-%m-%d %H:%M:%S"), delivery_id, product, qty])

shipping_df = pd.DataFrame(shipping_data, columns=["出荷日時", "納品番号", "製品名", "個数"])
shipping_df.to_csv(os.path.join(output_dir, "shipping_test.csv"), index=False)

print("✅ 生産・出荷データのCSVを生成しました → data/")
