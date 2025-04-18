from agv_env.inventory_env import InventoryEnv
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy

def main():
    env = InventoryEnv(render_mode="human")  # ← ここ！
    env = Monitor(env)

    model = DQN.load("models/dqn_inventory/inventory_dqn_model", env=env)
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=True)
    print(f"\n📊 評価結果：平均報酬 = {mean_reward:.2f}, 標準偏差 = {std_reward:.2f}")

if __name__ == "__main__":
    main()