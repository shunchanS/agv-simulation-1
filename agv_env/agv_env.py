# simulation/agv_env.py

import numpy as np
import random

class AGVEnv:
    def __init__(self, width=10, height=10, agv_count=3):
        self.width = width
        self.height = height
        self.agv_count = agv_count
        self.reset()

    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.agv_positions = [(0, self.height - 1) for _ in range(self.agv_count)]  # 左下からスタート
        self.kotatsu_locations = {}  # {(x, y): (product, qty)}
        self.product_stock = {}
        self.time = 0
        return self._get_observation()

    def _get_observation(self):
        return {
            "grid": self.grid.copy(),
            "agv_positions": list(self.agv_positions),
            "kotatsu": dict(self.kotatsu_locations),
            "stock": dict(self.product_stock),
            "time": self.time
        }

    def step(self, action):
        # 今後拡張：action = AGVの搬送指示 or 在庫配置
        self.time += 1
        return self._get_observation(), 0, False, {}