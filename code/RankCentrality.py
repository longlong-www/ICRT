import json
import numpy as np

CONFIG_FILE = 'configRankCentrality.json'

def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_win_matrix(data):
    """建立胜场矩阵 W[i,j] = i胜j次数"""
    players = sorted(set([m[0] for m in data] + [m[1] for m in data]))
    idx = {p: i for i, p in enumerate(players)}
    n = len(players)
    W = np.zeros((n, n), dtype=float)

    for p1, p2, w1, w2 in data:
        i, j = idx[p1], idx[p2]
        W[i, j] += w1
        W[j, i] += w2
    np.fill_diagonal(W, 0)
    return W, players

def rank_centrality(W):
    """严格复现 RankCentrality transition matrix + 稳态分布"""
    n = W.shape[0]
    P = np.zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(n):
            if i != j and (W[i, j] + W[j, i]) > 0:
                P[i, j] = (W[j, i] / (W[i, j] + W[j, i])) / (n - 1)
        # 对角线补充保证每行和为1
        P[i, i] = 1.0 - np.sum(P[i, :])

    # 幂迭代求稳态分布
    pi = np.ones(n) / n
    for _ in range(10000):
        new_pi = pi @ P
        if np.linalg.norm(new_pi - pi, 1) < 1e-12:
            break
        pi = new_pi
    pi /= pi.sum()
    return pi

# --- main ---
config = load_config(CONFIG_FILE)
data = config.get("data", [])

W, players = build_win_matrix(data)
scores = rank_centrality(W)  

ranked = sorted(zip(players, scores), key=lambda x: x[1], reverse=True)
print("RankCentrality Results:")
for name, score in ranked:
    print(f"{name}: {score:.4f}")

