import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os
import glob

def collect_data_from_csvs(directory_path):
    return glob.glob(os.path.join(directory_path, '*.csv'))

def charging_part(file_path):
    df = pd.read_csv(file_path)
    df['is_charging'] = df['Command'].str.contains('Charge')  # Identify charging instances
    df['charging_phase'] = (df['is_charging'] & ~df['is_charging'].shift(1).fillna(False)).cumsum()
    
    # Count unique charging cycles
    num_charging_cycles = df[df['is_charging']]['charging_phase'].nunique()
    print(f"Number of charging cycles: {num_charging_cycles}")
    
    charging_data = df[df['is_charging']].copy()
    charging_data['deltaV'] = charging_data.groupby('charging_phase')['U'].diff()
    charging_data['deltaAh'] = charging_data.groupby('charging_phase')['Ah'].diff()
    charging_data['dAh/dV'] = np.where(charging_data['deltaV'] != 0, charging_data['deltaAh'] / charging_data['deltaV'], np.nan)
    ICvalues=charging_data['dAh/dV'].copy()
    
    plt.figure(figsize=(10, 8))
    for phase in charging_data['charging_phase'].unique():
        phase_data = charging_data[charging_data['charging_phase'] == phase]
        plt.plot(phase_data['U'], phase_data['dAh/dV'], label=f'Phase {phase}')
    
    plt.xlabel('Voltage (U)')
    plt.ylabel('Incremental capacity [dAh/dV]')
    plt.title('IC curve')
    #plt.legend()
    plt.show()

    return df, num_charging_cycles , ICvalues

def plot_charging_phase(df, phase_number):

    phase_data = df[df['charging_phase'] == phase_number]
    if not phase_data.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(phase_data['Time'], phase_data['U'], label='Voltage (U)')
        plt.plot(phase_data['Time'], phase_data['Ah'], label='Capacity (Ah)')
        plt.xlabel('Time')
        plt.ylabel('[U]/[Ah]')
        plt.title(f'Voltage and Capacity during Charging Phase {phase_number}')
        plt.legend()
        plt.show()
    else:
        print(f"No data available for charging phase {phase_number}.")

'''

def plot_smoothed_ic_curve(charging_data,ICvalues):
    plt.figure(figsize=(10,8))

    for phase in charging_data['charging_phase'].unique():
        phase_data = charging_data[charging_data['charging_phase'] == phase]
        if len(phase_data) < 3:  # Skip if too few points for smoothing
            continue
        #phase_data['dAh/dV'] = phase_data['deltaAh'] / phase_data['deltaV']
        dAh_dV_smoothed = savgol_filter(ICvalues.dropna(), window_length=51, polyorder=3)
        plt.plot(phase_data['U'][1:-1], dAh_dV_smoothed, label=f'Phase {phase}')                       #ERROR TO BE RECTIFIED THE DIMENSION OF X AND Y IS NOT RIGHT 

    plt.xlabel('Voltage (U)')
    plt.ylabel('Smoothed Incremental Capacity (dAh/dV)')
    plt.title('Smoothed IC Curves')
    plt.legend()
    plt.show()

'''



def main():
    file_path = 'E:\\Thesis CEVT\\Dataset\\TUM\\Cyc01\\extracted_BW-VTC-429_3577_Cyc01_VV_20deg_BW-VTC-CYC.csv'
    df, num_charging_cycles, ICvalues = charging_part(file_path)
    print(f"The dataset contains {num_charging_cycles} charging cycles.")
    phase_number = 1  
    plot_charging_phase(df, phase_number)
    #plot_smoothed_ic_curve(df,ICvalues)
if __name__ == "__main__":
    main()
