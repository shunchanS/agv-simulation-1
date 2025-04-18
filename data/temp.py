import pandas as pd

# サンプル生産データ
data = {
    "開始時刻": [
        "2025-04-14 08:00",
        "2025-04-14 09:00",
        "2025-04-14 10:00"
    ],
    "終了時刻": [
        "2025-04-14 08:30",
        "2025-04-14 09:15",
        "2025-04-14 10:45"
    ],
    "製品名": ["P1", "P3", "P2"],
    "生産数": [30, 15, 24]
}

# DataFrame に変換
df = pd.DataFrame(data)

# 日時列を datetime に変換
df["開始時刻"] = pd.to_datetime(df["開始時刻"])
df["終了時刻"] = pd.to_datetime(df["終了時刻"])

# Excelファイルとして保存
df.to_excel("data/production_test.xlsx", index=False)

print("✅ production_test.xlsx を生成しました！")