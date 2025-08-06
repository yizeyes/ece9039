import os
import pydicom
import numpy as np
import cv2
from PIL import Image

def dcm_to_png(dcm_file_path, png_file_path, size=(512, 512)):
    # Read the DICOM file
    dcm = pydicom.dcmread(dcm_file_path)
    
    # Extract the pixel array from the DICOM file
    pixel_array = dcm.pixel_array
    
    # Normalize the pixel array to the range 0-255
    pixel_array = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
    
    # Convert the pixel array to uint8 type
    pixel_array = pixel_array.astype(np.uint8)
    
    # Resize the image to the desired size (512x512)
    resized_image = cv2.resize(pixel_array, size, interpolation=cv2.INTER_AREA)
    
    # Check if the image is grayscale or RGB
    if len(resized_image.shape) == 2:  # Grayscale image
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    elif len(resized_image.shape) == 3 and resized_image.shape[2] == 3:  # RGB image
        rgb_image = resized_image
    else:
        raise ValueError("Unsupported image format")
    
    # Save the image as PNG
    Image.fromarray(rgb_image).save(png_file_path)

def convert_all_dcm_to_png(directory_path, output_directory, size=(512, 512)):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.dcm'):
            dcm_file_path = os.path.join(directory_path, filename)
            png_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.png")
            dcm_to_png(dcm_file_path, png_file_path)
            print(f"Converted {dcm_file_path} to {png_file_path} with size 512x512 and color fidelity.")

# Example usage
directory_path = 'D:/NBIA/datasets/olddata'  # Path to the directory containing DICOM files
output_directory = 'D:/NBIA/datasets/datasets'  # Path to the directory where PNG files will be saved
convert_all_dcm_to_png(directory_path, output_directory)