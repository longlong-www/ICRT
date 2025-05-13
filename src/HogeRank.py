import numpy as np

# Match data
data = [
    ("ours", "jbk", 15, 5),
    ("ours", "deep", 15, 10),
    ("ours", "auto", 19, 12),
    ("ours", "art", 18, 7),
    ("ours", "code", 9, 6),
    ("jbk", "deep", 18, 12),
    ("jbk", "auto", 15, 10),
    ("jbk", "art", 20, 5),
    ("jbk", "code", 22, 3),
    ("deep", "auto", 18, 12),
    ("deep", "art", 19, 6),
    ("deep", "code", 22, 3),
    ("auto", "art", 19, 6),
    ("auto", "code", 21, 4),
    ("art", "code", 19, 6),
]

# 1. Generate player indices
players = set()
for match in data:
    players.add(match[0])
    players.add(match[1])

player_index = {player: i for i, player in enumerate(sorted(players))}
print("Player indices:")
for player, idx in player_index.items():
    print(f"{player}: {idx}")

# 2. Initialize design matrix A, observation vector y, and weight vector w
num_matches = len(data)
num_players = len(player_index)

A = np.zeros((num_matches, num_players))
y = np.zeros(num_matches)
w = np.zeros(num_matches)

# 3. Populate A, y, and w
for idx, (p1, p2, wins1, wins2) in enumerate(data):
    i, j = player_index[p1], player_index[p2]
    A[idx, i] = 1
    A[idx, j] = -1
    y[idx] = wins1 - wins2
    w[idx] = wins1 + wins2

    # Output processing results for each match
    print(f"Match {idx + 1}: {p1} vs {p2}")
    print(f"  {p1} wins: {wins1}, {p2} wins: {wins2}")
    print(f"  Design matrix A row: {A[idx]}")
    print(f"  Observation y: {y[idx]}")
    print(f"  Weight w: {w[idx]}")

# 4. Output the full A, y, and w
print("\nDesign matrix A:")
print(A)
print("\nObservation vector y:")
print(y)
print("\nWeight vector w:")
print(w)

# 5. Apply HodgeRank
def hodge_rank(A, y, w):
    W = np.diag(np.sqrt(w))
    P_inv = np.linalg.pinv(A.T @ W @ A)
    theta = P_inv @ A.T @ W @ y
    return theta

theta = hodge_rank(A, y, w)
print("\nRanking score vector theta:")
for player, score in sorted(player_index.items(), key=lambda x: theta[x[1]], reverse=True):
    print(f"{player}: {theta[player_index[player]]:.4f}")

# 6. Normalize ranking scores
theta_min, theta_max = np.min(theta), np.max(theta)
theta_normalized = (theta - theta_min) / (theta_max - theta_min)

# 7. Output normalized ranking score vector theta (range [0, 1])
print("\nNormalized ranking score vector theta (range [0, 1]):")
for player, score in sorted(player_index.items(), key=lambda x: theta_normalized[x[1]], reverse=True):
    print(f"{player}: {theta_normalized[player_index[player]]:.4f}")
