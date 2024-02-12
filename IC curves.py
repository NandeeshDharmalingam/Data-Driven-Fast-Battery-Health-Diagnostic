import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

# Correct file path for the uploaded file
file_path = r'E:\Thesis CEVT\Dataset\TUM\CU_Cyclic\CU000_cyc\New_BW-VTC-211_2229_CU_cyc_000_BW-VTC-CYC.csv'
data = pd.read_csv(file_path)

# The rest of the code is correctly set up for identifying discharge cycles and calculating dQ/dU

# Repeating necessary steps for context
data['DischargeFlag'] = data['I'] < 0
data['CycleId'] = (data['DischargeFlag'] & ~data['DischargeFlag'].shift(1).fillna(False)).cumsum()
discharge_data = data[data['DischargeFlag'] == True]
unique_cycle_ids = discharge_data['CycleId'].unique()

dq_du_data = pd.DataFrame()

for cycle_id in unique_cycle_ids:
    cycle_data = discharge_data[discharge_data['CycleId'] == cycle_id]
    if len(cycle_data) > 1:
        dQ = np.diff(cycle_data['Ah'].values)
        dU = np.diff(cycle_data['U'].values)
        valid_indices = dU != 0
        dQ = dQ[valid_indices]
        dU = dU[valid_indices]
        dQ_dU = dQ / dU
        U_mid = (cycle_data['U'].values[:-1] + cycle_data['U'].values[1:])/2
        U_mid = U_mid[valid_indices]
        cycle_dq_du_data = pd.DataFrame({'CycleId': cycle_id, 'dQ/dU': dQ_dU, 'U': U_mid})
        dq_du_data = pd.concat([dq_du_data, cycle_dq_du_data])

# Initial guess for window_length and poly_order
window_length, poly_order = 51,8  # Adjusting these based on the data's noise level and length

# Plotting dQ/dU vs U for all cycles with smoothing
plt.figure(figsize=(12, 8))

for cycle_id in dq_du_data['CycleId'].unique():
    cycle_dq_du = dq_du_data[dq_du_data['CycleId'] == cycle_id]
    if len(cycle_dq_du) > window_length:
        IC = cycle_dq_du['dQ/dU'].values
        # Applying Savitzky-Golay filter for smoothing
        try:
            smoothed_dq_du_IC = savgol_filter(IC, window_length, poly_order)
            plt.plot(cycle_dq_du['U'], smoothed_dq_du_IC, label=f'Cycle {cycle_id}')
        except ValueError:
            # This catches errors related to inappropriate window_length/poly_order for the data size
            print(f"Cycle {cycle_id}: Error in smoothing, check window_length/poly_order")

plt.xlabel('Voltage (U)')
plt.ylabel('Smoothed Incremental Capacity (dQ/dU)')
plt.title('Smoothed Incremental Capacity (dQ/dU) vs. Voltage (U) for Discharge Cycles')
plt.legend()
plt.grid(True)
plt.show()  
