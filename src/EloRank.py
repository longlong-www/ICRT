
import math

# Define initial parameters
methods = []
initial_rating = 1500  # Initial rating for all methods
K = 32                # ELO adjustment factor

# Initialize ratings
ratings = {method: initial_rating for method in methods}
print("Initial ratings:", ratings)  # Initial ratings

# Input data from the match statistics
data = [

]

# Function to calculate expected score
def expected_score(R1, R2):
    return 1 / (1 + math.pow(10, (R2 - R1) / 400))

# Batch update ratings
new_ratings = {method: 0 for method in methods}
print("New ratings (initialized to zero):", new_ratings)  # New ratings initialized to zero

for method1, method2, wins1, wins2 in data:
    print(f"\nMatch: {method1} vs {method2} | Wins: {wins1}-{wins2}")  # Match information
    total_matches = wins1 + wins2
    win_rate1 = wins1 / total_matches
    win_rate2 = wins2 / total_matches
    print(f"Win rates: {method1}={win_rate1:.2f}, {method2}={win_rate2:.2f}")  # Win rates

    R1, R2 = ratings[method1], ratings[method2]
    print(f"Current ratings: {method1}={R1}, {method2}={R2}")  # Current ratings

    E1 = expected_score(R1, R2)
    E2 = 1 - E1
    print(f"Expected scores: {method1}={E1:.2f}, {method2}={E2:.2f}")  # Expected scores

    # Accumulate rating adjustments
    adjustment1 = K * (win_rate1 - E1)
    adjustment2 = K * (win_rate2 - E2)
    print(f"Adjustments: {method1}={adjustment1:.2f}, {method2}={adjustment2:.2f}")  # Adjustments

    new_ratings[method1] += adjustment1
    new_ratings[method2] += adjustment2
    print(f"New ratings (accumulated): {method1}={new_ratings[method1]:.2f}, {method2}={new_ratings[method2]:.2f}")  # Accumulated new ratings

# Apply batch updates
print("\nApplying batch updates...")
for method in methods:
    ratings[method] += new_ratings[method]
    print(f"Updated rating for {method}: {ratings[method]:.2f}")  # Updated ratings

# Sort and display final ratings
sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
print("\nSorted final ratings:", sorted_ratings)  # Sorted final ratings
