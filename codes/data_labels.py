import pydicom
import os
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    boxes = []
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        xmax = int(bbox.find('xmax').text)
        ymin = int(bbox.find('ymin').text)
        ymax = int(bbox.find('ymax').text)
        label = obj.find('name').text
        boxes.append((xmin, ymin, xmax, ymax, label))
    return boxes

def convert_to_yolo_bbox(bbox, img_width, img_height):
    xmin, ymin, xmax, ymax, label = bbox
    x_center = ((xmin + xmax) / 2) / img_width
    y_center = ((ymin + ymax) / 2) / img_height
    width = (xmax - xmin) / img_width
    height = (ymax - ymin) / img_height
    return [label, x_center, y_center, width, height]  # Return label with bbox

def save_labels(labels, save_path):
    with open(save_path, 'w') as f:
        for label in labels:
            f.write(" ".join([str(x) for x in label]) + '\n')  # Use '\n' instead of '\\n'

def process_dataset(xml_dir, dcm_dir, df_dcm, data_dir, labels_dir):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)

    for index, row in df_dcm.iterrows():
        dcm_file_path = row['dcm_file']
        uid = row['uid_str']
        xml_file_path = os.path.join(xml_dir, uid + '.xml')
        if not os.path.exists(xml_file_path):
            continue
        boxes = parse_xml(xml_file_path)
        ds = pydicom.dcmread(dcm_file_path)
        img = ds.pixel_array
        labels = []
        for box in boxes:
            yolo_bbox = convert_to_yolo_bbox(box, img.shape[1], img.shape[0])
            # Convert label to a class index if needed, or keep it as is
            labels.append([yolo_bbox[0]] + yolo_bbox[1:])  # Use the label from the XML
        label_save_path = os.path.join(labels_dir, uid + '.txt')
        save_labels(labels, label_save_path)
        np.save(os.path.join(data_dir, uid + '.npy'), img)  # Saving the image as npy for simplicity

# Assuming you have df_dcm loaded as per your code
xml_dir = 'D:/NBIA/Lung-PET-CT-Dx-Annotations-XML-Files-rev12222020/Annotation/'
dcm_dir = 'D:/NBIA/manifest-1608669183333/Lung-PET-CT-Dx/'  # Assuming this is where dcm files are stored
data_dir = './data'
labels_dir = './labels'

process_dataset(xml_dir, dcm_dir, df_dcm, data_dir, labels_dir)
