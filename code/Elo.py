import json
import math

CONFIG_FILE = 'configElo.json'
def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

config = load_config(CONFIG_FILE)
methods = config.get("methods", [])
data = config.get("data", [])

initial_rating = 1500  # Initial rating for all methods
K = 32  # ELO adjustment factor

ratings = {method: initial_rating for method in methods}


def expected_score(R1, R2):
    return 1 / (1 + math.pow(10, (R2 - R1) / 400))

new_ratings = {method: 0 for method in methods}


for method1, method2, wins1, wins2 in data:
     
    total_matches = wins1 + wins2
    win_rate1 = wins1 / total_matches
    win_rate2 = wins2 / total_matches
    

    R1, R2 = ratings[method1], ratings[method2]
    

    E1 = expected_score(R1, R2)
    E2 = 1 - E1
    

    adjustment1 = K * (win_rate1 - E1)
    adjustment2 = K * (win_rate2 - E2)
    

    new_ratings[method1] += adjustment1
    new_ratings[method2] += adjustment2
     


for method in methods:
    ratings[method] += new_ratings[method]
    

sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
print("\nSorted ratings:", sorted_ratings) 