import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import ast

LOW_VALUE = 1e-6  # A small positive value to replace negative and zero values

# Function to extract features and targets with log scaling and handling negative/zero values
def extract_features_targets(df, n_days=5):
    features = []
    targets = []

    for index, row in df.iterrows():
        opens = row['Opens']
        highs = row['Highs']
        lows = row['Lows']
        closes = row['Closes']
        volumes = row['Volumes']

        dates = sorted(closes.keys())
        if len(dates) < n_days + 1:
            continue

        for i in range(len(dates) - n_days - 1):
            feature = []
            for j in range(i, i + n_days):
                date = dates[j]

                # Replace negative or zero values with LOW_VALUE
                feature.extend([
                    np.log1p(max(opens[date], LOW_VALUE)),
                    np.log1p(max(highs[date], LOW_VALUE)),
                    np.log1p(max(lows[date], LOW_VALUE)),
                    np.log1p(max(closes[date], LOW_VALUE)),
                    np.log1p(max(volumes[date], LOW_VALUE))
                ])

            next_day_price = max(closes[dates[i + n_days]], LOW_VALUE)
            current_day_price = max(closes[dates[i + n_days - 1]], LOW_VALUE)

            percentage_change = (np.log1p(next_day_price) - np.log1p(current_day_price)) / np.log1p(current_day_price) * 100

            features.append(feature)
            targets.append(percentage_change)

    return np.array(features), np.array(targets)

# Function to update the plot
def update_plot(x, y, ax):
    ax.clear()  # Clear the current plot
    ax.plot(x, y, marker='o')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Loss')
    ax.set_title('Training Progress')
    plt.pause(0.001)  # Pause for a short time to update the plot

# Read the CSV file
print("Loading data...")
df = pd.read_csv('data/DataFrame.csv')

# Parse string representations of dictionaries into actual dictionaries
print("Preprocessing data...")
df['Opens'] = df['Opens'].apply(ast.literal_eval)
df['Highs'] = df['Highs'].apply(ast.literal_eval)
df['Lows'] = df['Lows'].apply(ast.literal_eval)
df['Closes'] = df['Closes'].apply(ast.literal_eval)
df['Volumes'] = df['Volumes'].apply(ast.literal_eval)

# Extract features and targets
features, targets = extract_features_targets(df, n_days=5)

# Check distribution of features and targets
print(f"Features shape: {features.shape}")
print(f"Targets shape: {targets.shape}")
print(f"First few targets: {targets[:10]}")
print(f"First few features: {features[:5]}")

# No need to standardize features for GradientBoostingRegressor

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.3, random_state=42)

# Train a Gradient Boosting Regressor model
reg = GradientBoostingRegressor(random_state=42)

# Initialize lists to store loss for each iteration
iteration_losses = []

# Train the model with updates to the plot every 10 iterations
print("Training model...")
fig, ax = plt.subplots()
plt.ion()  # Turn on interactive mode for live updates
x_vals = []
y_vals = []

increment = 10

for i in range(0, len(X_train), increment):
    end_idx = min(i + increment, len(X_train))
    reg.fit(X_train[:end_idx], y_train[:end_idx])
    y_train_pred = reg.predict(X_train)
    loss = mean_squared_error(y_train, y_train_pred)
    iteration_losses.append(loss)
    x_vals.append(end_idx)
    y_vals.append(loss)
    update_plot(x_vals, y_vals, ax)
    print(f"Iteration {end_idx}: Loss = {loss}")

# Evaluate the model
y_pred = reg.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse:.2f}')
print(f'R^2 Score: {r2:.2f}')

plt.ioff()  # Turn off interactive mode
plt.show()  # Show the final plot
