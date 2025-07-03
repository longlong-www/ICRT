import json
import numpy as np

CONFIG_FILE = 'configHodgeRank.json'
def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

config = load_config(CONFIG_FILE)
data = config.get("data", [])

players = set()
for match in data:
    players.add(match[0])
    players.add(match[1])

player_index = {player: i for i, player in enumerate(sorted(players))}

# for player, idx in player_index.items():
#     print(f"{player}: {idx}")

num_matches = len(data)
num_players = len(player_index)

A = np.zeros((num_matches, num_players))
y = np.zeros(num_matches)
w = np.zeros(num_matches)

for idx, (p1, p2, wins1, wins2) in enumerate(data):
    i, j = player_index[p1], player_index[p2]
    A[idx, i] = 1
    A[idx, j] = -1
    y[idx] = wins1 - wins2
    w[idx] = wins1 + wins2

#     print(f"Match {idx + 1}: {p1} vs {p2}")
#     print(f"  {p1} Win Counts: {wins1}, {p2} Win Counts: {wins2}")
#     print(f"  Row of Design Matrix A: {A[idx]}")
#     print(f"  Observed Value y: {y[idx]}")
#     print(f"  Weight w: {w[idx]}")

# print("\nDesign Matrix A:")
# print(A)
# print("\nObservation Vector y:")
# print(y)
# print("\nWeight Vector w:")
# print(w)

def hodge_rank(A, y, w):
    W = np.diag(np.sqrt(w))
    P_Inv = np.linalg.pinv(A.T @ W @ A)
    theta = P_Inv @ A.T @ W @ y
    return theta

theta = hodge_rank(A, y, w)
print("\nRanking Score Vector (theta):")
for player, score in sorted(player_index.items(), key=lambda x: theta[x[1]], reverse=True):
    print(f"{player}: {theta[player_index[player]]:.4f}")

theta_min, theta_max = np.min(theta), np.max(theta)
theta_normalized = (theta - theta_min) / (theta_max - theta_min)

print("\nNormalized Ranking Score Vector (range [0, 1]):")
for player, score in sorted(player_index.items(), key=lambda x: theta_normalized[x[1]], reverse=True):
    print(f"{player}: {theta_normalized[player_index[player]]:.4f}")
