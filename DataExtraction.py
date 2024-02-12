
import os
import scipy.io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_and_save_mat_files(folder_path, columns_to_extract):
    csv_file_paths = []  # Store paths of created CSV files for later processing
    for file in os.listdir(folder_path):
        if file.endswith('.mat'):
            file_path = os.path.join(folder_path, file)
            mat_data = scipy.io.loadmat(file_path, squeeze_me=True, struct_as_record=False)
            dataset = mat_data.get('Dataset')
            if not dataset:
                print(f"No 'Dataset' found in {file}. Skipping.")
                continue

            data = {}
            array_lengths = {}

            for field in columns_to_extract:
                field_value = getattr(dataset, field, None)
                if field_value is not None:
                    if isinstance(field_value, np.ndarray):
                        data[field] = field_value.squeeze()
                        array_lengths[field] = len(data[field])
                    else:
                        data[field] = field_value
                        array_lengths[field] = 1

            if len(set(array_lengths.values())) == 1:
                df = pd.DataFrame(data)
                csv_file_name = 'New_' + os.path.splitext(file)[0] + '.csv'
                csv_file_path = os.path.join(folder_path, csv_file_name)
                df.to_csv(csv_file_path, index=False)
                csv_file_paths.append(csv_file_path)
                print(f"Processed and saved: {csv_file_name}")
            else:
                print(f"Skipping file '{file}' due to columns having different lengths.")
    return csv_file_paths


def main():
    # Define the columns you want to extract from cyclic ageging  
    columns_to_extract = [
        'Time', 'DataSet', 'tStep', 'Line', 'Command', 'U', 'I', 'Ah', 'AhStep', 'AhSet',
        'AhChSet', 'AhDisSet', 'Wh', 'WhStep', 'T1', 'RAC', 'RDC', 'CycCount', 'Count',
        'State', 'i_cut_hi', 'i_cut_lo', 'i_cut_low', 'i_cut_high'
    ]

#    columns_to_extract = [
#        'Time', 'DataSet', 'tStep', 'Line', 'Command', 'U', 'I', 'Ah', 'AhStep', 'AhSet',
#        'Wh', 'T1', 'RAC', 'RDC', 'CycCount', 'State']
    folder_path = 'E:\Thesis CEVT\Dataset\TUM\CYC_Cyclic'
    for subdir, dirs, files in os.walk(folder_path, topdown=True):
        for folder_name in dirs:
            if folder_name.endswith("Cyc01"):
                specific_folder_path = os.path.join(subdir, folder_name)
                csv_file_paths = extract_and_save_mat_files(specific_folder_path, columns_to_extract)
            else:
                print("check the path or the name of the file again")

    


if __name__ == "__main__":
    main()
