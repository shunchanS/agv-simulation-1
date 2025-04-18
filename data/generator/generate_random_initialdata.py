import pandas as pd
import random
from datetime import datetime

# 製品リスト（P1〜P10）
products = [f"P{i+1}" for i in range(10)]

# 保管マス（こたつ）50個にランダムに配置（P1〜P10が均等に含まれるように）
kotatsu_positions = [(x, y) for y in range(2, 7) for x in range(11)]  # y=2〜6, x=0〜10 → 最大55マス
random.shuffle(kotatsu_positions)
kotatsu_positions = kotatsu_positions[:50]

# 各製品が最低1個以上は在庫を持つように初期割当
initial_inventory = []
assigned = {p: False for p in products}

for pos in kotatsu_positions:
    if False in assigned.values():
        # まだ割り当てられてない製品を優先的に選ぶ
        product = random.choice([p for p in products if not assigned[p]])
        assigned[product] = True
    else:
        product = random.choice(products)
    qty = random.randint(5, 30)
    initial_inventory.append({
        "X": pos[0],
        "Y": pos[1],
        "製品名": product,
        "在庫数": qty
    })

# DataFrame にして CSV 出力
df_inventory = pd.DataFrame(initial_inventory)
df_inventory.to_csv("data/initial_inventory.csv", index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="初期在庫データ", dataframe=df_inventory)