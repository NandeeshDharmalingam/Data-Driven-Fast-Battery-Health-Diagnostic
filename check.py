import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib 
import sys
import numpy as np 
import pandas as pd
import os
import pickle
import random
from os import listdir
import tensorflow as tf
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
# import keras_tuner as kt
from tensorflow import keras
from timeit import default_timer as timer  
import seaborn as sns
from scipy.io import loadmat
from pykalman import KalmanFilter

CU_list = listdir('E:\Thesis CEVT\Dataset\TUM\CU_Cyclic')
CU_list.sort()
print(CU_list)

out_data = dict()
for CU_id in tqdm(CU_list):
    Cell_file = listdir(f'E:\Thesis CEVT\Dataset\TUM\CU_Cyclic\{CU_id}')
    for cell in Cell_file:
        if '.mat' in cell:
            file_path = f'E:\Thesis CEVT\Dataset\TUM\CU_Cyclic\{CU_id}{cell}'
            mat_data = loadmat(file_path, squeeze_me=True, struct_as_record=False)
            columns_to_extract = [
                'Time', 'DataSet', 'tStep', 'Line', 'Command', 'U', 'I', 'Ah', 'AhStep', 'AhSet',
                 'Wh',  'T1', 'RAC', 'RDC', 'CycCount', 
                'State']
            dataset = mat_data.get('Dataset')
            data = {}
            for field in columns_to_extract:
                field_value = getattr(dataset, field, None)
                if field_value is not None:
                    if isinstance(field_value, np.ndarray):
                        data[field] = field_value.squeeze()
            df = pd.DataFrame(data)
            if df['Time'].iloc[-1] < 100:
                df['Time'] = df['Time']*3600

            discharge_1 = df[(df['Command']=='Discharge') & (df['Line']==20) | (df['Line']==21)]
            discharge_2 = df[(df['Command']=='Discharge') & (df['Line']==27) | (df['Line']==28)]
            dis_cap_1 = -sum(discharge_1['Time'].diff().iloc[1:]*discharge_1['I'].iloc[1:])/3600
            dis_cap_2 = -sum(discharge_2['Time'].diff().iloc[1:]*discharge_2['I'].iloc[1:])/3600
            dis_cap = (dis_cap_1 + dis_cap_2) / 2
            charge_1 = df[(df['Command']=='Charge') & (df['Line']==16) | (df['Line']==17)]
            charge_2 = df[(df['Command']=='Charge') & (df['Line']==23) | (df['Line']==24)]
            cha_cap_1 = sum(charge_1['Time'].diff().iloc[1:]*charge_1['I'].iloc[1:])/3600
            cha_cap_2 = sum(charge_2['Time'].diff().iloc[1:]*charge_2['I'].iloc[1:])/3600
            cha_cap = (cha_cap_1 + cha_cap_2) / 2

            if f'{cell[7:10]}' in out_data.keys():
                out_data[f'{cell[7:10]}']['Capacity_dis'].append(dis_cap)
                out_data[f'{cell[7:10]}']['Capacity_cha'].append(cha_cap)
                out_data[f'{cell[7:10]}']['Current'].append(charge_2['I'].values)
                out_data[f'{cell[7:10]}']['Voltage'].append(charge_2['U'].values)
                out_data[f'{cell[7:10]}']['Temperature'].append(charge_2['T1'].values)
                out_data[f'{cell[7:10]}']['Time'].append(charge_2['Time'].values)
            else:
                out_data[f'{cell[7:10]}'] = dict()
                out_data[f'{cell[7:10]}']['Capacity_dis'] = [dis_cap]
                out_data[f'{cell[7:10]}']['Capacity_cha'] = [cha_cap]
                out_data[f'{cell[7:10]}']['Current'] = [charge_2['I'].values]
                out_data[f'{cell[7:10]}']['Voltage'] = [charge_2['U'].values]
                out_data[f'{cell[7:10]}']['Temperature'] = [charge_2['T1'].values]
                out_data[f'{cell[7:10]}']['Time'] = [charge_2['Time'].values]


colors = plt.cm.jet(np.linspace(0,0.5,len(out_data[cell_id]['Voltage'])))
for cell_id in out_data.keys():
    plt.figure(figsize=[10, 6])
    print(f"{cell_id} ICA analysis")

    for cycle_index, voltage in enumerate(out_data[cell_id]['Voltage']):
        current = out_data[cell_id]['Current'][cycle_index]
        time = out_data[cell_id]['Time'][cycle_index]

        # Calculate dQ and dV, ensure arrays are prepared properly
        time_diff = np.diff(time, prepend=time[0])
        dQ = current * time_diff / 3600  # Ah
        dV = np.diff(voltage, prepend=voltage[0])
        dq_dv = np.divide(dQ, dV, out=np.zeros_like(dQ), where=dV!=0)
        

        # Apply Kalman Filter to dQ/dV
        kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1, n_dim_state=1,
                          transition_matrices=[1], observation_matrices=[1],
                          initial_state_covariance=1, observation_covariance=1,
                          transition_covariance=0.1)
        dq_dv_filtered, _ = kf.filter(dq_dv.reshape(-1, 1))

        # Ensure the voltage array is prepared for plotting
        # Trimming or adjusting voltage array based on filtered dQ/dV length
        voltage_for_plot = voltage[1:len(dq_dv_filtered.ravel())+1]

        if len(voltage_for_plot) != len(dq_dv_filtered.ravel()):
            # If lengths still don't match, further adjust to ensure exact match
            min_length = min(len(voltage_for_plot), len(dq_dv_filtered.ravel()))
            voltage_for_plot = voltage_for_plot[:min_length]
            dq_dv_filtered = dq_dv_filtered[:min_length]

        plt.plot(voltage_for_plot, dq_dv_filtered.ravel(), color=colors[cycle_index],label=f'Cycle {cycle_index+1}')


    plt.xlabel('Voltage (V)')
    plt.ylabel('dQ/dV (Filtered)')
    plt.title(f'ICA Analysis for Cell {cell_id}')
    plt.show()