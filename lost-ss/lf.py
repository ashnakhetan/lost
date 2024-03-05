import pandas as pd
import numpy as np

# Load CSV files
users_df = pd.read_csv('LF_Traveler.csv')  # Replace with your file path
items_df = pd.read_csv('LF_Attraction.csv')  # Replace with your file path

# Convert to NumPy arrays (assuming 'user_id' and 'item_id' are columns in your CSV)
# Ensure these are integer indices
user_ids = users_df['Traveler_ID'].values
item_ids = items_df['Attraction_ID'].values

# Initialize P and Q matrices
num_users = len(np.unique(user_ids))
num_items = len(np.unique(item_ids))
num_factors = len(users_df)

P = np.random.normal(0, 0.1, (num_users, num_factors))
Q = np.random.normal(0, 0.1, (num_items, num_factors))

# Placeholder for your training data
# Assuming 'train' is an object that provides user, item, and rating data
train = ...  # Load or define your training dataset here

alpha = 0.01  # Learning rate
num_epochs = 10  # Number of epochs

# Matrix Factorization Algorithm
for epoch in range(num_epochs):
    for u, i, r_ui in train.all_ratings():  # Replace 'train.all_ratings()' with actual method to get user-item-rating tuples
        residual = r_ui - np.dot(P[u], Q[i])
        temp = P[u, :]  # Temporary variable for simultaneous update
        P[u, :] += alpha * residual * Q[i]
        Q[i, :] += alpha * residual * temp

# P and Q are now the factorized matrices
