import os
import xml.etree.ElementTree as ET

# Mapping for labels
label_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}

# Function to convert XML to YOLO format
def convert_xml_to_yolo(xml_file, output_folder):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return
    
    yolo_lines = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        label_num = label_mapping.get(name, -1)
        
        if label_num == -1:
            print(f"Warning: Unmapped label '{name}' in {xml_file}")
            continue

        bndbox = obj.find('bndbox')
        if bndbox is None:
            print(f"Warning: No bounding box in {xml_file} for object '{name}'")
            continue

        try:
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            x_center = ((xmin + xmax) / 2) / 512.0
            y_center = ((ymin + ymax) / 2) / 512.0
            width = (xmax - xmin) / 512.0
            height = (ymax - ymin) / 512.0

            yolo_lines.append(f"{label_num} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        except Exception as e:
            print(f"Error processing bounding box in {xml_file}: {e}")

    if yolo_lines:
        base_name = os.path.basename(xml_file).replace('.xml', '.txt')
        output_file = os.path.join(output_folder, base_name)
        with open(output_file, 'w') as f:
            f.writelines(yolo_lines)
        print(f"Converted {xml_file} to {output_file}")

# Define source and paths for XML
xml_source_path = 'D:/NBIA/Lung-PET-CT-Dx-Annotations-XML-Files-rev12222020/Annotation'
yolo_output_path = 'D:/NBIA/labels'

# Create directory if it doesn't exist
os.makedirs(yolo_output_path, exist_ok=True)

# Iterate through XML files and convert them
for root, dirs, files in os.walk(xml_source_path):
    for file in files:
        if file.endswith('.xml'):
            xml_file_path = os.path.join(root, file)
            convert_xml_to_yolo(xml_file_path, yolo_output_path)

print("XML to YOLO complete.")
