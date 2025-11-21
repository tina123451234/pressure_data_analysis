import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Load the data
file_path = "/Users/tina/Desktop/pressure_data/NMC_RPT_data/NMC_RPT_0_Single_Cycle_with_SOC.xlsx"
df = pd.read_excel(file_path)

# Create a copy for processing
data = df.copy()

# Identify cycles based on capacity resets and current direction
# A new cycle starts when capacity drops significantly (reset to ~0)
data['capacity_reset'] = (data['Capacity(Ah)'].diff() < -0.1).astype(int)
data['cycle_id'] = data['capacity_reset'].cumsum()

# Separate charging and discharging cycles
charging_data = data[data['Current(A)'] > 0].copy()
discharging_data = data[data['Current(A)'] < 0].copy()

# Function to calculate SOC for each cycle
def calculate_soc(group, mode='charge'):
    capacity = group['Capacity(Ah)'].values
    max_capacity = capacity.max()
    
    if max_capacity > 0:
        if mode == 'charge':
            # Charging: SOC goes from 0 to 1
            soc = capacity / max_capacity
        else:
            # Discharging: SOC goes from 1 to 0
            soc = 1 - (capacity / max_capacity)
    else:
        soc = np.zeros_like(capacity)
    
    group['SOC'] = soc
    return group

# Calculate SOC for charging cycles
charging_cycles = charging_data.groupby('cycle_id', group_keys=False).apply(
    lambda x: calculate_soc(x, mode='charge')
)

# Calculate SOC for discharging cycles
discharging_cycles = discharging_data.groupby('cycle_id', group_keys=False).apply(
    lambda x: calculate_soc(x, mode='discharge')
)

# Function to calculate dP/dQ with smoothing options
def calculate_dpdq(group, smooth=True, window_length=11, polyorder=3):
    pressure = group['pressure_cDAQ1Mod4/ai2'].values
    capacity = group['Capacity(Ah)'].values
    
    # Optional: smooth the raw data first
    if smooth and len(pressure) > window_length:
        pressure = savgol_filter(pressure, window_length, polyorder)
    
    # Calculate differences
    dp = np.diff(pressure)
    dq = np.diff(capacity)
    
    # Use a larger threshold to avoid noise from tiny capacity changes
    dq[np.abs(dq) < 1e-4] = np.nan
    dpdq = dp / dq
    
    # Add NaN at the beginning to maintain array length
    dpdq = np.concatenate([[np.nan], dpdq])
    
    # Optional: apply additional smoothing to the derivative
    if smooth and len(dpdq) > window_length:
        valid_mask = np.isfinite(dpdq)
        if valid_mask.sum() > window_length:
            dpdq_smooth = np.full_like(dpdq, np.nan)
            dpdq_smooth[valid_mask] = savgol_filter(dpdq[valid_mask], window_length, polyorder)
            dpdq = dpdq_smooth
    
    group['dP/dQ'] = dpdq
    return group

# Calculate dP/dQ for both charging and discharging
charging_cycles = charging_cycles.groupby('cycle_id', group_keys=False).apply(calculate_dpdq)
discharging_cycles = discharging_cycles.groupby('cycle_id', group_keys=False).apply(calculate_dpdq)

# Create figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Battery Cycling Analysis: Pressure vs State of Charge', fontsize=16, fontweight='bold')

# Get unique cycle IDs
charging_cycle_ids = charging_cycles['cycle_id'].unique()
discharging_cycle_ids = discharging_cycles['cycle_id'].unique()

# Color maps for different cycles
colors = plt.cm.viridis(np.linspace(0, 1, max(len(charging_cycle_ids), len(discharging_cycle_ids))))

# Plot 1: Pressure vs SOC (Charging)
ax1 = axes[0, 0]
for i, cycle_id in enumerate(charging_cycle_ids):
    cycle_data = charging_cycles[charging_cycles['cycle_id'] == cycle_id]
    ax1.plot(cycle_data['SOC'], cycle_data['pressure_cDAQ1Mod4/ai2'], 
             label=f'Cycle {cycle_id}', color=colors[i], linewidth=1.5, alpha=0.7)
ax1.set_xlabel('State of Charge (SOC)', fontsize=12)
ax1.set_ylabel('Pressure', fontsize=12)
ax1.set_title('Charging: Pressure vs SOC', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 1)

# Plot 2: Pressure vs SOC (Discharging)
ax2 = axes[0, 1]
for i, cycle_id in enumerate(discharging_cycle_ids):
    cycle_data = discharging_cycles[discharging_cycles['cycle_id'] == cycle_id]
    ax2.plot(cycle_data['SOC'], cycle_data['pressure_cDAQ1Mod4/ai2'], 
             label=f'Cycle {cycle_id}', color=colors[i], linewidth=1.5, alpha=0.7)
ax2.set_xlabel('State of Charge (SOC)', fontsize=12)
ax2.set_ylabel('Pressure', fontsize=12)
ax2.set_title('Discharging: Pressure vs SOC', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1, 0)  # Reverse x-axis for discharging

# Plot 3: dP/dQ vs SOC (Charging)
ax3 = axes[1, 0]
for i, cycle_id in enumerate(charging_cycle_ids):
    cycle_data = charging_cycles[charging_cycles['cycle_id'] == cycle_id]
    # Filter out extreme outliers and invalid values
    dpdq = cycle_data['dP/dQ']
    soc = cycle_data['SOC']
    
    # More aggressive filtering: use IQR method
    valid_mask = np.isfinite(dpdq)
    if valid_mask.sum() > 0:
        q1 = np.percentile(dpdq[valid_mask], 25)
        q3 = np.percentile(dpdq[valid_mask], 75)
        iqr = q3 - q1
        lower_bound = q1 - 3 * iqr
        upper_bound = q3 + 3 * iqr
        valid_mask = valid_mask & (dpdq >= lower_bound) & (dpdq <= upper_bound)
    
    if valid_mask.sum() > 0:
        ax3.plot(soc[valid_mask], dpdq[valid_mask], 
                 label=f'Cycle {cycle_id}', color=colors[i], linewidth=2, alpha=0.8)
ax3.set_xlabel('State of Charge (SOC)', fontsize=12)
ax3.set_ylabel('dP/dQ', fontsize=12)
ax3.set_title('Charging: dP/dQ vs SOC (Smoothed)', fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, 1)

# Plot 4: dP/dQ vs SOC (Discharging)
ax4 = axes[1, 1]
for i, cycle_id in enumerate(discharging_cycle_ids):
    cycle_data = discharging_cycles[discharging_cycles['cycle_id'] == cycle_id]
    # Filter out extreme outliers and invalid values
    dpdq = cycle_data['dP/dQ']
    soc = cycle_data['SOC']
    
    # More aggressive filtering: use IQR method
    valid_mask = np.isfinite(dpdq)
    if valid_mask.sum() > 0:
        q1 = np.percentile(dpdq[valid_mask], 25)
        q3 = np.percentile(dpdq[valid_mask], 75)
        iqr = q3 - q1
        lower_bound = q1 - 3 * iqr
        upper_bound = q3 + 3 * iqr
        valid_mask = valid_mask & (dpdq >= lower_bound) & (dpdq <= upper_bound)
    
    if valid_mask.sum() > 0:
        ax4.plot(soc[valid_mask], dpdq[valid_mask], 
                 label=f'Cycle {cycle_id}', color=colors[i], linewidth=2, alpha=0.8)
ax4.set_xlabel('State of Charge (SOC)', fontsize=12)
ax4.set_ylabel('dP/dQ', fontsize=12)
ax4.set_title('Discharging: dP/dQ vs SOC (Smoothed)', fontsize=13, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.set_xlim(1, 0)  # Reverse x-axis for discharging

plt.tight_layout()
plt.savefig('battery_cycling_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Print summary statistics
print(f"\nAnalysis Summary:")
print(f"Total charging cycles: {len(charging_cycle_ids)}")
print(f"Total discharging cycles: {len(discharging_cycle_ids)}")

