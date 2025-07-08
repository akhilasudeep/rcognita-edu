import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('simdata', exist_ok=True)

# Define Gain values k
gain_sets = [
    {"k_rho": 4.0, "k_alpha": 7.0, "k_beta": -1.2},
    {"k_rho": 0.8, "k_alpha": 3.0, "k_beta": -1.5},
]

csv_files = [
    '/home/akhila/Desktop/rcognita-edu-main-20250701T235226Z-1-001/rcognita-edu-main/simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-06-22_17h17m02s__run01.csv',
    '/home/akhila/Desktop/rcognita-edu-main-20250701T235226Z-1-001/rcognita-edu-main/simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-06-22_17h17m02s__run02.csv',
]


colors = ['purple', 'brown']

def smart_read_csv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("t [s],"):
            header_index = i
            break
    return pd.read_csv(file_path, skiprows=header_index)

# PLOT 1: robot trajectories vs reference
plt.figure(figsize=(6, 6))
for i, (file, color) in enumerate(zip(csv_files, colors)):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]
    label = f'Run {i+1}: k_rho={gain_sets[i]["k_rho"]}, k_alpha={gain_sets[i]["k_alpha"]}, k_beta={gain_sets[i]["k_beta"]}'
    plt.plot(data['x [m]'], data['y [m]'], label=label, color=color)

plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('Robot Trajectories (Kinematic Controller)')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.savefig('simdata/Robot_Trajectories_Kinematics.png')
plt.close()

# PLOT 2: linear velocity vs time
plt.figure(figsize=(6, 6))
for i, (file, color) in enumerate(zip(csv_files, colors)):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]
    plt.plot(data['t [s]'], data['v [m/s]'], label=f'Run {i+1}', color=color)

plt.xlabel('t [s]')
plt.ylabel('v [m/s]')
plt.title('Linear Velocity Over Time')
plt.legend()
plt.grid(True)
plt.savefig('simdata/Linear_Velocity_Kinematics.png')
plt.close()

# PLOT 3: omega vs time
plt.figure(figsize=(6, 6))
for i, (file, color) in enumerate(zip(csv_files, colors)):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]
    plt.plot(data['t [s]'], data['omega [rad/s]'], label=f'Run {i+1}', color=color)

plt.xlabel('t [s]')
plt.ylabel('omega [rad/s]')
plt.title('Angular Velocity Over Time')
plt.legend()
plt.grid(True)
plt.savefig('simdata/Angular_Velocity_Kinematics.png')
plt.close()

# PLOT 4: tracking error vs time
x_goal, y_goal = 0.0, 0.0 

plt.figure(figsize=(6, 6))
for i, (file, color) in enumerate(zip(csv_files, colors)):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]
    error = np.sqrt((data['x [m]'] - x_goal)**2 + (data['y [m]'] - y_goal)**2)
    plt.plot(data['t [s]'], error, label=f'Run {i+1}', color=color)

plt.xlabel('t [s]')
plt.ylabel('Tracking Error [m]')
plt.title('Tracking Error Over Time')
plt.legend()
plt.grid(True)
plt.savefig('simdata/Tracking_Error_Over_Time.png')
plt.close()

print("success!!!")