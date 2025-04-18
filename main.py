from data_loader.shipping import load_shipping_csv
from data_loader.production import load_production_csv
from data_loader.inventory import load_initial_inventory
from config.settings import AREA_WIDTH, AREA_HEIGHT
from simulation.simulator import run_simulation, generate_kotatsu_positions
from visualization.drawer import draw_map
import random


def main():
    print("AGV Simulation Start")

    # 出荷・生産・初期在庫データ読み込み
    shipping_df = load_shipping_csv("data/shipping_test.csv")
    production_df = load_production_csv("data/production_test.csv")
    initial_df = load_initial_inventory("data/initial_inventory.csv")

    print("\n▼ 出荷データの先頭5件")
    print(shipping_df.head())

    print("\n▼ 生産データの先頭5件")
    print(production_df.head())

    print("\n▼ 初期在庫の先頭5件")
    print(initial_df.head())

    shipping_ports = [(i * (AREA_WIDTH - 1) // 6, 0) for i in range(7)]
    kotatsu_list = generate_kotatsu_positions(AREA_WIDTH, AREA_HEIGHT)
    kotatsu_list.sort(key=lambda pos: min(abs(pos[0] - port[0]) + abs(pos[1] - port[1]) for port in shipping_ports))

    # 初期在庫を配置
    kotatsu_storage = {}
    agv_kotatsu_paths = []
    free_kotatsu = kotatsu_list.copy()

    for idx, row in initial_df.iterrows():
        if not free_kotatsu:
            print("⚠️ 初期在庫の配置先が足りません")
            break
        pos = free_kotatsu.pop(0)
        start = (pos[0], AREA_HEIGHT - 1)
        path = [start, pos]
        kotatsu_storage[pos] = (row["製品名"], row["在庫数"])
        agv_kotatsu_paths.append(path)

    # 生産品を追加保管
    for idx, row in production_df.iterrows():
        if not free_kotatsu:
            print("⚠️ 保管エリア満杯！")
            break
        pos = free_kotatsu.pop(0)
        start = (pos[0], AREA_HEIGHT - 1)
        path = [start, pos]
        if pos in kotatsu_storage:
            prod, qty = kotatsu_storage[pos]
            kotatsu_storage[pos] = (prod, qty + row["生産数"])
        else:
            kotatsu_storage[pos] = (row["製品名"], row["生産数"])
        agv_kotatsu_paths.append(path)

    # 出荷処理
    agv_shipping_paths = []
    for idx, row in shipping_df.iterrows():
        product = row["製品名"]
        quantity = row["個数"]
        candidates = [pos for pos, (p, q) in kotatsu_storage.items() if p == product and q > 0]
        if not candidates:
            print(f"⚠️ 出荷失敗：{product} の在庫がありません")
            continue
        pos = candidates[0]
        nearest_port = min(shipping_ports, key=lambda p: abs(p[0] - pos[0]) + abs(p[1] - pos[1]))
        path = [pos, nearest_port]
        agv_shipping_paths.append(path)
        kotatsu_storage[pos] = (product, max(0, kotatsu_storage[pos][1] - quantity))

    all_paths = agv_kotatsu_paths + agv_shipping_paths
    draw_map(kotatsu_storage, shipping_ports, all_paths, AREA_WIDTH, AREA_HEIGHT)


if __name__ == "__main__":
    main()