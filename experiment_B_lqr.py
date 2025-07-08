import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import glob

# Define cost matrices Q and R
cost_sets = [
    {"Q": [12.0, 6.0, 18.0], "R": [5.0, 5.0]},
    {"Q": [50.0, 25.0, 50.0], "R": [8.0, 8.0]},
    {"Q": [10.0, 5.0, 2.0], "R": [0.2, 0.2]}
]

log_folder = "/home/akhila/Desktop/rcognita-edu-main-20250701T235226Z-1-001/rcognita-edu-main/simdata/lqr/Init_angle_1.57_seed_1_Nactor_10/"
os.makedirs(log_folder, exist_ok=True)

for i, cost in enumerate(cost_sets):
    print(f"\n🔁 Running LQR Simulation {i+1} with Q={cost['Q']} and R={cost['R']}")

    os.environ["Q_VALS"] = " ".join(str(x) for x in cost["Q"])
    os.environ["R_VALS"] = " ".join(str(x) for x in cost["R"])

    subprocess.run([
        "python3", "PRESET_3wrobot_NI.py",
        "--ctrl_mode", "lqr",
        "--Nruns", "1",
        "--t1", "20",
        "--is_visualization", "0",
        "--is_log_data", "1",
        "--Q", *map(str, cost["Q"]),
        "--R", *map(str, cost["R"]),
        "--v_max", "1.0",
        "--omega_max", "1.0"
    ])

def find_latest_lqr_csvs(folder, prefix="3wrobotNI_lqr_", run_suffix="__run01.csv", count=3):
    pattern = os.path.join(folder, f"{prefix}*{run_suffix}")
    all_files = glob.glob(pattern)
    all_files.sort(key=os.path.getmtime, reverse=True)
    return all_files[:count]

print("\n📊 Plotting Results...")

csvs = find_latest_lqr_csvs(log_folder)

if not csvs:
    print("❌ No CSV files found for plotting.")
    exit()

def smart_read_csv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("t [s],"):
            header_index = i
            break
    return pd.read_csv(file_path, skiprows=header_index)

dfs = [smart_read_csv(f) for f in csvs]
print(f"✅ Found {len(dfs)} CSV files for plotting.")


colors = ['blue', 'brown', 'yellow']

# PLOT 1: trajectories
plt.figure(figsize=(6, 6))
for i, df in enumerate(dfs):
    plt.plot(df['x [m]'], df['y [m]'], label=f"Run {i+1} - Q={cost_sets[i]['Q']}, R={cost_sets[i]['R']}", color=colors[i])
plt.title("LQR: Trajectory (x vs y)")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "Trajectory_Plot.png"))
plt.close()

# PLOT 2: tracking reeor vs time
plt.figure(figsize=(6, 6))
for i, df in enumerate(dfs):
    error = np.sqrt(df['x [m]']**2 + df['y [m]']**2)
    plt.plot(df['t [s]'], error, label=f"Run {i+1}", color=colors[i])
    if error.iloc[-1] > 0.5:
        print(f"⚠️  Run {i+1} may not have converged: final error = {error.iloc[-1]:.2f} m")

plt.title("LQR: Tracking Error vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Position Error [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "Tracking_Error_Plot.png"))
plt.close()

# PLOT 3: v and omega vs time
plt.figure(figsize=(6, 6))
for i, df in enumerate(dfs):
    plt.plot(df['t [s]'], df['v [m/s]'], label=f"v - Run {i+1}", color=colors[i])
    plt.plot(df['t [s]'], df['omega [rad/s]'], '--', label=f"ω - Run {i+1}", color=colors[i])
plt.title("LQR: Control Inputs Over Time")
plt.xlabel("Time [s]")
plt.ylabel("Input Values")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "Control_Inputs_Plot.png"))
plt.close()

print("Success!!!")
