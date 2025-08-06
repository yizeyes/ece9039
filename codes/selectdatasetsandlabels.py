import os
import shutil

def compare_and_move_files(folder1, folder2, unmatched_folder):
    # Ensure the unmatched folder exists
    os.makedirs(unmatched_folder, exist_ok=True)

    # Get files without extensions
    files_in_folder1 = {os.path.splitext(f)[0]: f for f in os.listdir(folder1)}
    files_in_folder2 = {os.path.splitext(f)[0]: f for f in os.listdir(folder2)}

    # Find common and unique files by name (without extension)
    common_files = set(files_in_folder1.keys()).intersection(set(files_in_folder2.keys()))
    unique_files_folder1 = set(files_in_folder1.keys()) - common_files
    unique_files_folder2 = set(files_in_folder2.keys()) - common_files

    # Process common files
    for base_name in common_files:
        print(f"Keeping common file: {files_in_folder1[base_name]} and {files_in_folder2[base_name]}")

    # Move unique files from folder1
    for base_name in unique_files_folder1:
        src_path = os.path.join(folder1, files_in_folder1[base_name])
        dest_path = os.path.join(unmatched_folder, files_in_folder1[base_name])
        shutil.move(src_path, dest_path)
        print(f"Moved unique file from folder1 to unmatched folder: {files_in_folder1[base_name]}")

    # Move unique files from folder2
    for base_name in unique_files_folder2:
        src_path = os.path.join(folder2, files_in_folder2[base_name])
        dest_path = os.path.join(unmatched_folder, files_in_folder2[base_name])
        shutil.move(src_path, dest_path)
        print(f"Moved unique file from folder2 to unmatched folder: {files_in_folder2[base_name]}")

# Example usage
folder1_path = 'D:/NBIA/datasets/datasets'
folder2_path = 'D:/NBIA/datasets/labels'
unmatched_folder_path = 'D:/NBIA/datasets/nolabels'

compare_and_move_files(folder1_path, folder2_path, unmatched_folder_path)
