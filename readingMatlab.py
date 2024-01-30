import os
import scipy.io
import pandas as pd
import numpy as np

def extract_and_save_mat_files(folder_path, columns_to_extract):
    for file in os.listdir(folder_path):
        if file.endswith('.mat'):
            # Construct the full file path
            file_path = os.path.join(folder_path, file)
            # Load the .mat file
            mat_data = scipy.io.loadmat(file_path)
            # Extract the 'Dataset' key
            dataset = mat_data['Dataset']

            # Create a dictionary to store the extracted data
            data = {}

            # Initialize an array to store the lengths of fields
            array_lengths = {}

            # Iterate through the columns to extract
            for field in columns_to_extract:
                if isinstance(dataset[field], np.ndarray):
                    # If the field is an array, extract and store it
                    data[field] = dataset[field][0][0].squeeze()
                    # Get the length of the array
                    array_lengths[field] = len(data[field])
                else:
                    # If it's not an array, store it as is
                    data[field] = dataset[field]
                    # Set a default length of 1
                    array_lengths[field] = 1

            # Check if all arrays have the same length
            if len(set(array_lengths.values())) == 1:
                # Convert the dictionary to a DataFrame
                df = pd.DataFrame(data)
                # Define the CSV file path (change 'extracted_' to any prefix you prefer)
                csv_file_name = 'extracted_' + os.path.splitext(file)[0] + '.csv'
                csv_file_path = os.path.join(folder_path, csv_file_name)
                # Save the DataFrame to a CSV file
                df.to_csv(csv_file_path, index=False)
                print(f"Processed and saved: {csv_file_name}")
            else:
                print(f"Skipping file '{file}' due to columns having different lengths.")

# Define the columns you want to extract
columns_to_extract = [
    'Time', 'DataSet', 'tStep', 'Line', 'Command', 'U', 'I', 'Ah', 'AhStep', 'AhSet',
    'AhChSet', 'AhDisSet', 'Wh', 'WhStep', 'T1', 'RAC', 'RDC', 'CycCount', 'Count',
    'State', 'i_cut_hi', 'i_cut_lo', 'i_cut_low', 'i_cut_high'
]

folder_path = 'E:\Thesis CEVT\Dataset\TUM\Cyc01'
cyclepath='E:\Thesis CEVT\Dataset\TUM'
extract_and_save_mat_files(folder_path, columns_to_extract)
