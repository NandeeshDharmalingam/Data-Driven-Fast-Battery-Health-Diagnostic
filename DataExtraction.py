import os
import scipy.io
import csv
import numpy as np

# Specify the directory containing MAT files
mat_directory = "E:\Thesis CEVT\Dataset\TUM\CU_calander\CU_Calendar\CU000"

# Get a list of all MAT files in the directory
mat_files = [file for file in os.listdir(mat_directory) if file.endswith('.mat')]

# Iterate through each MAT file
for mat_file in mat_files:
    # Load the MAT file into a Python dictionary
    mat_path = os.path.join(mat_directory, mat_file)
    mat = scipy.io.loadmat(mat_path)

    # Extract all data from the MAT file
    data = {}
    try:
        dataset = mat['Dataset'][0, 0]
        for field_name in dataset.dtype.names:
            value = dataset[field_name]
            if isinstance(value, np.ndarray) and value.ndim > 1:
                # If the value is a 2D array, store each column in a separate key
                for i in range(value.shape[1]):
                    column_name = f"{field_name}_{i + 1}"
                    data[column_name] = value[:, i].tolist()
            else:
                # For other cases, store the data as is
                data[field_name] = value.tolist() if isinstance(value, np.ndarray) else value
    except KeyError:
        print(f"KeyError: 'Dataset' not found in {mat_file}.")

    # Write the data to a CSV file with the same name as the MAT file
    csv_file = os.path.splitext(mat_file)[0] + '.csv'
    csv_path = os.path.join(mat_directory, csv_file)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        header = list(data.keys())
        writer.writerow(header)

        # Write data column-wise
        max_len = max(len(value) if isinstance(value, (list, tuple)) else 1 for value in data.values())
        for i in range(max_len):
            row = [data[key][i] if isinstance(data[key], (list, tuple)) and i < len(data[key]) else data[key] for key in header]
            writer.writerow(row)

    print(f"All data extracted from {mat_file} and saved to {csv_file}.")
