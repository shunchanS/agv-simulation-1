import random
from config.settings import AGV_COUNT, AREA_WIDTH, AREA_HEIGHT
from simulation.utils import calc_distance

def generate_kotatsu_positions(area_width, area_height):
    """
    保管エリア内のこたつ位置（製品を置けるマス）を生成する関数
    :param area_width: 横のマス数（例：10）
    :param area_height: 縦のマス数（例：10）
    :return: こたつ位置のリスト（例：[(0,2), (1,2), ..., (9,6)]）
    """
    kotatsu_positions = []
    for y in range(2, 7):  # y=2〜6 の5行をこたつエリアとする
        for x in range(area_width):
            kotatsu_positions.append((x, y))
    return kotatsu_positions

def run_simulation(products, shipping_ports):
    # 在庫配置
    storage = {}
    for product, freq in products.items():
        needed_qty = freq
        while needed_qty > 0:
            x = random.randint(0, AREA_WIDTH - 1)
            y = random.randint(1, AREA_HEIGHT - 1)  # y=0は出荷口のため除外
            if (x, y) not in storage:
                store_qty = min(36, needed_qty)
                storage[(x, y)] = [product, store_qty]
                needed_qty -= store_qty

    # 出荷依頼生成
    total_requests = []
    for product, freq in products.items():
        interval = 28800 // freq
        for t in range(0, 28800, interval):
            total_requests.append((t, product))
    total_requests.sort()

    agvs = [0] * AGV_COUNT
    agv_paths = []
    total_distance = 0
    total_time = 0

    for req_time, product in total_requests:
        available_locations = [pos for pos, val in storage.items() if val[0] == product and val[1] > 0]
        if not available_locations:
            continue
        location = available_locations[0]
        agv_id = min(range(AGV_COUNT), key=lambda i: max(agvs[i], req_time))
        start_time = max(agvs[agv_id], req_time)
        nearest_port = min(shipping_ports, key=lambda p: calc_distance(location, p))

        dist = calc_distance(location, nearest_port)
        time_taken = dist * 1.0  # AGV_SPEED

        agv_paths.append([location, nearest_port])
        agvs[agv_id] = start_time + time_taken
        storage[location][1] -= 1
        total_distance += dist
        total_time = max(total_time, agvs[agv_id])

    return storage, agv_paths, total_distance, total_time