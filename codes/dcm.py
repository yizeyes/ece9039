import os
import pandas as pd
import shutil
import pydicom

# Load the CSV file to match filenames with UIDs
csv_file_path = 'D:/NBIA/dcm_file_uid.csv'
csv_data = pd.read_csv(csv_file_path)

# Specify the source and destination paths
source_dcm_path = 'D:/NBIA/manifest-1608669183333/Lung-PET-CT-Dx'
annotation_path = 'D:/NBIA/Lung-PET-CT-Dx-Annotations-XML-Files-rev12222020/Annotation'
destination_path = 'D:/NBIA/FilteredDCMFiles'

# Create destination directory if it doesn't exist
os.makedirs(destination_path, exist_ok=True)

# Iterate through subdirectories and files to find matching UIDs
for root, dirs, files in os.walk(source_dcm_path):
    for file in files:
        if file.endswith('.dcm'):
            file_path = os.path.join(root, file)
            # Read the DICOM file to get its UID
            dicom_data = pydicom.dcmread(file_path)
            file_uid = dicom_data.SOPInstanceUID
            
            # Check if the UID is present in the CSV and corresponding annotation directory
            if any(csv_data['uid'] == file_uid):
                for ann_root, ann_dirs, ann_files in os.walk(annotation_path):
                    for ann_file in ann_files:
                        if file_uid in ann_file:
                            # If UID is found, copy the file
                            shutil.copy(file_path, os.path.join(destination_path, f"{file_uid}.dcm"))
                            print(f"File {file} with UID {file_uid} is copied to the destination folder.")

print("DICOM filtering and copying complete.")
