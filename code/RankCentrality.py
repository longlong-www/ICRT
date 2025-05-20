import json
import numpy as np

CONFIG_FILE = 'configRankCentrality.json'

def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def spectral_ranking(w, n):

    P = w / np.sum(w, axis=1, keepdims=True)
    # print(P)
    P = np.nan_to_num(P) 
    eigvals, eigvecs = np.linalg.eig(P.T)
    idx = np.argmax(np.real(eigvals))
    Pi = np.abs(np.real(eigvecs[:, idx]))
    # print(Pi / np.sum(Pi))

    return Pi / np.sum(Pi)

def process_match_data(data):

    players = sorted(set([match[0] for match in data] + [match[1] for match in data]))
    player_indices = {player: i for i, player in enumerate(players)}
    n = len(players)

    A = np.zeros((n, n))
    for player1, player2, wins1, wins2 in data:
        i, j = player_indices[player1], player_indices[player2]
        A[i, j] = wins2
        A[j, i] = wins1
    
    return A, players

config = load_config(CONFIG_FILE)
data = config.get("data", [])

A, players = process_match_data(data)

ranking = spectral_ranking(A, len(players))

ranked_players = sorted(zip(players, ranking), key=lambda x: x[1], reverse=True)
print("Ranking Results:")
for player, score in ranked_players:
    print(f"{player}: {score:.4f}")
