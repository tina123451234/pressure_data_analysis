import pandas as pd
import numpy as np

# File path
file_path = "/Users/tina/Desktop/pressure_data/NMC_RPT_data/NMC_RPT_0_single_cycle.xlsx"

# Load the data
print("Loading data...")
df = pd.read_excel(file_path, sheet_name='Sheet1')

print(f"\nColumns loaded from file: {len(df.columns)}")
print(df.columns.tolist())

# Clean column names - remove leading/trailing spaces and normalize
df.columns = df.columns.str.strip()

print(f"Data shape: {df.shape}")
print("\n=== Column Names ===")
for i, col in enumerate(df.columns):
    print(f"{i}: '{col}'")

# Find columns flexibly
def find_column(df, keywords):
    """Find column containing any of the keywords (case insensitive)"""
    for col in df.columns:
        col_lower = col.lower()
        if any(kw.lower() in col_lower for kw in keywords):
            return col
    return None

capacity_col = find_column(df, ['capacity', 'cap'])
current_col = find_column(df, ['current', 'curr'])
step_col = find_column(df, ['step type', 'step_type', 'steptype'])

if capacity_col is None:
    print("\nERROR: Could not find Capacity column!")
    print("Available columns:", df.columns.tolist())
    exit()

if current_col is None:
    print("\nERROR: Could not find Current column!")
    print("Available columns:", df.columns.tolist())
    exit()

print(f"\nUsing columns:")
print(f"  Capacity: '{capacity_col}'")
print(f"  Current: '{current_col}'")
if step_col:
    print(f"  Step Type: '{step_col}'")

# Initialize SOC calculation
print("\n=== Calculating SOC ===")

df['SOC_calculated'] = 0.0
cumulative_charge = 0.0

for i in range(len(df)):
    current_capacity = df.loc[i, capacity_col]
    current_val = df.loc[i, current_col]
    
    if i == 0:
        df.loc[i, 'SOC_calculated'] = 0.0
        prev_capacity = current_capacity
    else:
        prev_capacity_val = df.loc[i-1, capacity_col]
        
        # Check if capacity reset (new step started)
        if current_capacity < prev_capacity_val - 0.001:
            prev_capacity = 0.0
        
        # Calculate the change from previous row
        capacity_change = current_capacity - prev_capacity
        
        # Update cumulative charge based on current direction
        if current_val > 0.01:
            # Charging - SOC increases
            cumulative_charge += capacity_change
        elif current_val < -0.01:
            # Discharging - SOC decreases
            cumulative_charge -= capacity_change
        
        prev_capacity = current_capacity
        df.loc[i, 'SOC_calculated'] = cumulative_charge

print("\n=== SOC Calculation Complete ===")
print(f"SOC range: {df['SOC_calculated'].min():.4f} to {df['SOC_calculated'].max():.4f} Ah")

# Display sample data
print("\n=== Sample Data (first 10 rows) ===")
cols_to_show = [current_col, capacity_col, 'SOC_calculated']
if step_col:
    cols_to_show.append(step_col)
print(df[cols_to_show].head(10))

print("\n=== Checking transitions ===")
df['Capacity_diff'] = df[capacity_col].diff()
reset_indices = df[df['Capacity_diff'] < -0.01].index.tolist()

if len(reset_indices) > 0:
    print(f"\nFound {len(reset_indices)} capacity resets (step transitions)")
    
    # Show first 3 transitions
    for idx in reset_indices[:3]:
        print(f"\nTransition at index {idx}:")
        display_cols = [current_col, capacity_col, 'SOC_calculated', 'Capacity_diff']
        if step_col:
            display_cols.append(step_col)
        print(df[display_cols].loc[max(0, idx-2):idx+3])

# Verification
print("\n=== Verification ===")
charge_data = df[df[current_col] > 0.01]
discharge_data = df[df[current_col] < -0.01]

if len(charge_data) > 0:
    print(f"SOC during charging: {charge_data['SOC_calculated'].min():.4f} to {charge_data['SOC_calculated'].max():.4f} Ah")
if len(discharge_data) > 0:
    print(f"SOC during discharging: {discharge_data['SOC_calculated'].min():.4f} to {discharge_data['SOC_calculated'].max():.4f} Ah")

# Check for large jumps
df['SOC_diff'] = df['SOC_calculated'].diff()
large_jumps = df[np.abs(df['SOC_diff']) > 0.01]
print(f"\nNumber of SOC changes > 0.01 Ah: {len(large_jumps)}")

# Save the file
output_path = "/Users/tina/Desktop/pressure_data/NMC_RPT_data/NMC_RPT_0_Single_Cycle_with_SOC.xlsx"
df.to_excel(output_path, index=False)
print(f"\n=== File saved ===")
print(f"Saved to: {output_path}")