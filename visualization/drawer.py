import matplotlib.pyplot as plt
import time

def draw_map(storage, shipping_ports, agv_paths, AREA_WIDTH, AREA_HEIGHT):
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(-1, AREA_WIDTH)
    ax.set_ylim(-1, AREA_HEIGHT)
    ax.set_xticks(range(AREA_WIDTH))
    ax.set_yticks(range(AREA_HEIGHT))
    ax.grid(True)

    # 出荷口の描画（赤い点）
    for port in shipping_ports:
        ax.plot(port[0], port[1], 'ro')

    # 保管マスの描画（ラベル付き）
    for (x, y), (product, qty) in storage.items():
        ax.text(x, y, product, ha='center', va='center', fontsize=8,
                bbox=dict(boxstyle="round", facecolor="lightblue"))

    # AGVのパスを1つずつ描画（ちょっとずつ時間を空ける）
    for path in agv_paths:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]

        color = 'blue' if path[0][1] == AREA_HEIGHT - 1 else 'red'
        linestyle = '--'
        ax.plot(xs, ys, linestyle=linestyle, color=color, alpha=0.7)

        # ↓ ここが肝心：少し待ってから次の線を描画
        plt.pause(0.05)

    ax.set_title("AGV搬送シミュレーション（青=保管 / 赤=出荷）")
    plt.gca().invert_yaxis()
    plt.show()