import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import ast

LOW_VALUE = 1e-6  # A small positive value to replace negative and zero values

# Function to extract features and targets with log scaling and handling negative/zero values
def extract_features_targets(df, n_days=252, days_ahead=23):
    features = []
    targets = []

    for index, row in df.iterrows():
        opens = row['Opens']
        highs = row['Highs']
        lows = row['Lows']
        closes = row['Closes']
        volumes = row['Volumes']

        dates = sorted(closes.keys())
        if len(dates) < n_days + days_ahead:
            continue

        for i in range(len(dates) - n_days - days_ahead):
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

            next_day_price = max(closes[dates[i + n_days + days_ahead - 1]], LOW_VALUE)
            current_day_price = max(closes[dates[i + n_days - 1]], LOW_VALUE)

            # Calculate percentage change without log scaling
            percentage_change = (next_day_price - current_day_price) / current_day_price * 100

            features.append(feature)
            targets.append(percentage_change)

    return np.array(features), np.array(targets)

# Function to update the plot
def update_plot(x, r2_values, mse_values):
    plt.clf()  # Clear the current plot
    plt.plot(x, r2_values, marker='o', label='R² Score')
    plt.plot(x, mse_values, marker='x', label='MSE')
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Training Progress')
    plt.legend()
    plt.draw()  # Draw the updated plot
    plt.pause(0.001)  # Pause for a short time to update the plot

# Parameters for the prediction
n_days = 5  # Number of days used for the prediction
days_ahead = 1  # Number of days ahead to predict

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

# Limit the dataset size for testing
#df = df.head(10000)  # Limit to the first 10,000 rows

features, targets = extract_features_targets(df, n_days=n_days, days_ahead=days_ahead)

# Check number of samples
print(f"Total samples: {features.shape[0]}")

# Standardize the features
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.3, random_state=42)

# Train a Random Forest regressor with reduced complexity
reg = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)

# Initialize lists to store R² scores and MSE for each iteration
iteration_r2_scores = []
iteration_mse_values = []
x_vals = []

# Train the model with updates to the plot every 100 iterations
print("Training model...")
plt.ion()  # Turn on interactive mode for live updates
fig, ax = plt.subplots()

increment = 100  # Update the plot every 100 samples

for i in range(0, len(X_train), increment):
    end_idx = min(i + increment, len(X_train))
    reg.fit(X_train[:end_idx], y_train[:end_idx])
    y_train_pred = reg.predict(X_train[:end_idx])
    r2 = r2_score(y_train[:end_idx], y_train_pred)
    mse = mean_squared_error(y_train[:end_idx], y_train_pred)
    iteration_r2_scores.append(r2)
    iteration_mse_values.append(mse)
    x_vals.append(end_idx)
    update_plot(x_vals, iteration_r2_scores, iteration_mse_values)
    print(f"Iteration {end_idx}: R² Score = {r2:.2f}, MSE = {mse:.2f}")

# Evaluate the model
y_pred = reg.predict(X_test)
test_r2 = r2_score(y_test, y_pred)
test_mse = mean_squared_error(y_test, y_pred)
print(f'R² Score on Test Data: {test_r2:.2f}')
print(f'MSE on Test Data: {test_mse:.2f}')

plt.ioff()  # Turn off interactive mode
plt.show()  # Show the final plot
