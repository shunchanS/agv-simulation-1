from agv_env.inventory_env import InventoryEnv

env = InventoryEnv()
obs, _ = env.reset()

for step in range(10):
    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    print(f"Step {step+1}: Action = {action}, Reward = {reward}")
    env.render()