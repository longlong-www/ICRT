import numpy as np

def spectral_ranking(w: np.ndarray, n: int) -> np.ndarray:
    """
    Compute spectral ranking using the Rank Centrality algorithm.

    Parameters:
        w (numpy.ndarray): Win-count transition matrix of shape (n x n).
        n (int): Number of players.

    Returns:
        numpy.ndarray: Probability distribution of rankings (Pi).
    """
    # Build the normalized transition probability matrix
    P = w / np.sum(w, axis=1, keepdims=True)
    print(P)
    # Replace possible NaNs (from division by zero) with zeros
    P = np.nan_to_num(P)

    # Perform eigen-decomposition on the transpose of P
    eigvals, eigvecs = np.linalg.eig(P.T)
    
    # Select the eigenvector corresponding to the largest real eigenvalue
    idx = np.argmax(np.real(eigvals))
    Pi = np.abs(np.real(eigvecs[:, idx]))
    # Normalize to get a proper probability distribution
    print(Pi / np.sum(Pi))
    return Pi / np.sum(Pi)

def process_match_data(data: list[tuple[str, str, int, int]]) -> tuple[np.ndarray, list[str]]:
    """
    Convert match results into a win-count transition matrix.

    Parameters:
        data (list of tuples): Each entry is
            (player1, player2, player1_wins, player2_wins).

    Returns:
        A (numpy.ndarray): Win-count transition matrix of shape (n x n).
        players (list): List of player names.
    """
    # Gather all unique player names and assign each an index
    players = sorted({match[0] for match in data} | {match[1] for match in data})
    player_indices = {player: i for i, player in enumerate(players)}
    n = len(players)

    # Initialize the win-count matrix to zeros
    A = np.zeros((n, n), dtype=int)

    # Populate the matrix:
    # A[i, j] = number of times player j defeated player i
    for p1, p2, wins1, wins2 in data:
        i, j = player_indices[p1], player_indices[p2]
        A[i, j] = wins2
        A[j, i] = wins1
    
    return A, players

# Match results data
data = [
    ("ours", "jbk", 20, 5),
    ("ours", "deep", 15, 10),
    ("ours", "auto", 17, 8),
    ("ours", "art", 18, 7),
    ("ours", "code", 19, 6),
    ("jbk", "deep", 13, 12),
    ("jbk", "auto", 15, 10),
    ("jbk", "art", 20, 5),
    ("jbk", "code", 22, 3),
    ("deep", "auto", 13, 12),
    ("deep", "art", 19, 6),
    ("deep", "code", 22, 3),
    ("auto", "art", 19, 6),
    ("auto", "code", 21, 4),
    ("art", "code", 19, 6),
]

# Process the match data into a transition matrix
A, players = process_match_data(data)

# Compute the spectral ranking
ranking = spectral_ranking(A, len(players))

# Sort and display the ranking results
ranked_players = sorted(
    zip(players, ranking),
    key=lambda x: x[1],
    reverse=True
)

print("Ranking Results:")
for player, score in ranked_players:
    print(f"{player}: {score:.4f}")
