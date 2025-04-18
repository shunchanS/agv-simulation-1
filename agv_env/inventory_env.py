import numpy as np
import gymnasium as gym
from gymnasium import spaces

class InventoryEnv(gym.Env):
    def __init__(self, width=10, height=10, num_products=10, max_steps=100):
        super(InventoryEnv, self).__init__()

        self.width = width
        self.height = height
        self.num_products = num_products
        self.max_steps = max_steps
        self.current_step = 0

        self.start_pos = (0, height - 1)
        self.shipping_ports = [(i, 0) for i in range(width)]

        self.grid = np.zeros((height, width), dtype=int)
        self.inventory = {}

        self.action_space = spaces.Discrete(width * height)
        self.observation_space = spaces.Dict({
            "grid": spaces.Box(low=0, high=num_products, shape=(height, width), dtype=int),
            "inventory": spaces.Box(low=0, high=999, shape=(num_products,), dtype=int)
        })

        self.current_product = 0
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.grid[:] = 0
        self.inventory.clear()
        self.current_step = 0
        self.current_product = 0
        return self._get_obs(), {}

    def _get_obs(self):
        inventory_array = np.zeros(self.num_products, dtype=int)
        for _, (pid, qty) in self.inventory.items():
            inventory_array[pid] += qty
        return {
            "grid": self.grid.copy(),
            "inventory": inventory_array
        }

    def step(self, action):
        x = action % self.width
        y = action // self.width

        reward = 0
        done = False

        if self.grid[y, x] == 0:
            self.grid[y, x] = self.current_product + 1
            self.inventory[(x, y)] = (self.current_product, 1)
            dist = min(abs(x - px) + abs(y - py) for px, py in self.shipping_ports)
            reward = max(0, 10 - dist)
            self.current_product = (self.current_product + 1) % self.num_products
        else:
            reward = -1

        self.current_step += 1
        if self.current_step >= self.max_steps:
            done = True

        return self._get_obs(), reward, done, False, {}

    def render(self):
        for y in range(self.height):
            row = " ".join(f"{self.grid[y,x]:2}" for x in range(self.width))
            print(row)
        print("-" * 20)
