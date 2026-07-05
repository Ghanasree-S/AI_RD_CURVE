import numpy as np
import pandas as pd
from scipy.optimize import minimize

df = pd.read_csv('xy_data.csv')

x_data = df['x'].values
y_data = df['y'].values

n_points = len(df)
t_data = np.linspace(6, 60, n_points)

def l1_loss(params):
    theta, M, X = params
    
    x_pred = t_data * np.cos(theta) - np.exp(M * np.abs(t_data)) * np.sin(0.3 * t_data) * np.sin(theta) + X
    y_pred = 42 + t_data * np.sin(theta) + np.exp(M * np.abs(t_data)) * np.sin(0.3 * t_data) * np.cos(theta)
    
    loss_x = np.sum(np.abs(x_data - x_pred))
    loss_y = np.sum(np.abs(y_data - y_pred))
    
    return loss_x + loss_y

# Convert theta bounds from degrees to radians
theta_min = np.radians(0)
theta_max = np.radians(50)

# Define bounds based on the assignment criteria
bounds = [
    (theta_min, theta_max),  # Theta bounds
    (-0.05, 0.05),           # M bounds
    (0, 100)                 # X bounds
]

initial_guess = [np.radians(25), 0.0, 50.0]

result = minimize(l1_loss, initial_guess, bounds=bounds, method='Powell')

best_theta_rad, best_M, best_X = result.x
best_theta_deg = np.degrees(best_theta_rad)

print("--- Optimization Results ---")
print(f"Theta (Radians): {best_theta_rad:.4f}  (Degrees: {best_theta_deg:.2f}°)")
print(f"M: {best_M:.4f}")
print(f"X: {best_X:.4f}")
print(f"Minimum L1 Loss achieved: {result.fun:.4f}")