import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
 
def plot_voltage_pressure_combined(file_path, 
                                 time_column="pressure_Time", 
                                 voltage_column="Voltage(V)", 
                                 pressure_column=None):
    
    
    print("="*50)
    print("COMBINED VOLTAGE & PRESSURE PLOT")
    print("="*50)
    
    # Load Excel file
    try:
        print(f"Loading data from: {file_path}")
        df = pd.read_excel(file_path)
        print(f"✓ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    # Handle pressure column (default = column T / index 19 if not provided)
    if pressure_column is None:
        try:
            pressure_data = pd.to_numeric(df.iloc[:, 19], errors="coerce")  # column T
            pressure_column = df.columns[19]
        except Exception as e:
            print(f"Error: Could not read pressure column from Excel column T. {e}")
            return None
    else:
        if pressure_column not in df.columns:
            print(f"\nError: Column '{pressure_column}' not found.")
            return None
        pressure_data = pd.to_numeric(df[pressure_column], errors="coerce")
    
    # Extract time and voltage
    required_cols = [time_column, voltage_column]
    for col in required_cols:
        if col not in df.columns:
            print(f"\nError: Column '{col}' not found in file!")
            return None
    
    time_data = pd.to_datetime(df[time_column], errors="coerce")
    voltage_data = pd.to_numeric(df[voltage_column], errors="coerce")
    
    # Clean rows - keep only valid data points
    valid_mask = ~(time_data.isna() | voltage_data.isna() | pressure_data.isna())
    
    time_data = time_data[valid_mask]
    voltage_data = voltage_data[valid_mask]
    pressure_data = pressure_data[valid_mask]
    
    if len(time_data) == 0:
        print("Error: No valid data points found after cleaning!")
        return None
    
    print(f"✓ Final dataset: {len(time_data)} valid data points")

    # Save directory
    output_dir = os.path.dirname(file_path) or "."
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create combined plot with dual y-axes
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Plot voltage on primary y-axis
    line1 = ax1.plot(time_data, voltage_data, 'o-', color='blue', linewidth=2, 
                     markersize=3, alpha=0.7, label='Voltage (V)')
    ax1.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Voltage (V)', fontsize=12, fontweight='bold', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True, alpha=0.3)
    
    # Create secondary y-axis for pressure
    ax2 = ax1.twinx()
    line2 = ax2.plot(time_data, pressure_data, 's-', color='red', linewidth=2, 
                     markersize=3, alpha=0.7, label=f'Pressure ({pressure_column})')
    ax2.set_ylabel('Pressure', fontsize=12, fontweight='bold', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Format x-axis for datetime
    if pd.api.types.is_datetime64_any_dtype(time_data):
        fig.autofmt_xdate()
    
    # Add title
    plt.title('Voltage and Pressure over Time', fontsize=16, fontweight='bold', pad=20)
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', 
               fontsize=11, framealpha=0.9)
    
    plt.tight_layout()
    
    # Save plot as SVG
    combined_svg = os.path.join(output_dir, f"{base_name}_voltage_pressure_combined.svg")
    plt.savefig(combined_svg, format='svg', bbox_inches='tight', facecolor='white')
    print(f"✓ Combined plot saved: {combined_svg}")
    plt.show()
    
    # Print summary statistics
    print(f"\n📊 Data Summary:")
    print(f"  Time range: {time_data.min()} to {time_data.max()}")
    print(f"  Voltage range: {voltage_data.min():.3f}V to {voltage_data.max():.3f}V")
    print(f"  Pressure range: {pressure_data.min():.3f} to {pressure_data.max():.3f}")
    
    return None


# Alternative version with more pronounced non-continuous styling
def plot_voltage_pressure_scatter(file_path, 
                                time_column="pressure_Time", 
                                voltage_column="Voltage(V)", 
                                pressure_column=None):
    """
    Plot voltage and pressure vs time as scatter plots (completely non-continuous).
    
    Parameters:
    - file_path: Path to the Excel file
    - time_column: Name of the time column (default: "pressure_Time")
    - voltage_column: Name of the voltage column (default: "Voltage(V)")
    - pressure_column: Name of the pressure column (default: None, will use Excel column T if not provided)
    """
    
    print("="*50)
    print("SCATTER PLOT: VOLTAGE & PRESSURE")
    print("="*50)
    
    # Load Excel file
    try:
        print(f"Loading data from: {file_path}")
        df = pd.read_excel(file_path)
        print(f"✓ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    # Handle pressure column
    if pressure_column is None:
        try:
            pressure_data = pd.to_numeric(df.iloc[:, 19], errors="coerce")  # column T
            pressure_column = df.columns[19]
        except Exception as e:
            print(f"Error: Could not read pressure column from Excel column T. {e}")
            return None
    else:
        if pressure_column not in df.columns:
            print(f"\nError: Column '{pressure_column}' not found.")
            return None
        pressure_data = pd.to_numeric(df[pressure_column], errors="coerce")
    
    # Extract time and voltage
    required_cols = [time_column, voltage_column]
    for col in required_cols:
        if col not in df.columns:
            print(f"\nError: Column '{col}' not found in file!")
            return None
    
    time_data = pd.to_datetime(df[time_column], errors="coerce")
    voltage_data = pd.to_numeric(df[voltage_column], errors="coerce")
    
    # Clean rows
    valid_mask = ~(time_data.isna() | voltage_data.isna() | pressure_data.isna())
    
    time_data = time_data[valid_mask]
    voltage_data = voltage_data[valid_mask]
    pressure_data = pressure_data[valid_mask]
    
    if len(time_data) == 0:
        print("Error: No valid data points found after cleaning!")
        return None
    
    print(f"✓ Final dataset: {len(time_data)} valid data points")

    # Save directory
    output_dir = os.path.dirname(file_path) or "."
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create scatter plot with dual y-axes
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Plot voltage as scatter points on primary y-axis
    scatter1 = ax1.scatter(time_data, voltage_data, c='blue', s=20, alpha=0.6, 
                          label='Voltage (V)', marker='o')
    ax1.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Voltage (V)', fontsize=12, fontweight='bold', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True, alpha=0.3)
    
    # Create secondary y-axis for pressure
    ax2 = ax1.twinx()
    scatter2 = ax2.scatter(time_data, pressure_data, c='red', s=20, alpha=0.6, 
                          label=f'Pressure ({pressure_column})', marker='s')
    ax2.set_ylabel('Pressure', fontsize=12, fontweight='bold', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Format x-axis for datetime
    if pd.api.types.is_datetime64_any_dtype(time_data):
        fig.autofmt_xdate()
    
    # Add title
    plt.title('Voltage and Pressure over Time (Scatter Plot)', fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    ax1.legend(['Voltage (V)'], loc='upper left', fontsize=11, framealpha=0.9)
    ax2.legend([f'Pressure ({pressure_column})'], loc='upper right', fontsize=11, framealpha=0.9)
    
    plt.tight_layout()
    
    # Save plot as SVG
    scatter_svg = os.path.join(output_dir, f"{base_name}_voltage_pressure_scatter.svg")
    plt.savefig(scatter_svg, format='svg', bbox_inches='tight', facecolor='white')
    print(f"✓ Scatter plot saved: {scatter_svg}")
    plt.show()
    
    return None


# Example usage
if __name__ == "__main__":
    file_path = '/Users/tina/Desktop/pressure_data/NMC_RPT_data/NMC_RPT_0_Single_Cycle_with_SOC.xlsx'
    
    # Option 1: Line plot with markers (slightly non-continuous)
    print("Creating combined line plot...")
    plot_voltage_pressure_combined(file_path)
    
    # Option 2: Pure scatter plot (completely non-continuous)
    print("\nCreating scatter plot...")
    plot_voltage_pressure_scatter(file_path)
    
    print("\n" + "="*50)
    print("✓ ALL PLOTS COMPLETED")
    print("="*50)