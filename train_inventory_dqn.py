from agv_env.inventory_env import InventoryEnv
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy

import os

def main():
    # 環境の初期化
    env = InventoryEnv()

    # モデルの保存先ディレクトリ
    model_dir = "models/dqn_inventory"
    os.makedirs(model_dir, exist_ok=True)

    # モデルの初期化
    model = DQN("MultiInputPolicy", env, verbose=1, tensorboard_log="./tensorboard_log")

    # 学習（例：10000ステップ）
    model.learn(total_timesteps=10000)

    # モデル保存
    model.save(f"{model_dir}/dqn_inventory")

    # 学習済みモデルの読み込み（確認用）
    model = DQN.load(f"{model_dir}/dqn_inventory", env=env)

    # 評価（10エピソード）
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"評価結果: 平均報酬 = {mean_reward}, 標準偏差 = {std_reward}")

if __name__ == "__main__":
    main()