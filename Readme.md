---

## 📘 **README: Medical Image Processing and Annotation Pipeline**

This repository contains a set of Python scripts designed for preprocessing, cleaning, and converting DICOM medical images and their XML annotations into formats suitable for machine learning training, particularly YOLO object detection.

---

### 📂 **Module Descriptions**

#### ✅ `data_labels.py`

**Function:**

* Parses bounding boxes from XML annotation files.
* Converts bounding boxes to YOLO format (`x_center`, `y_center`, `width`, `height` normalized by image size).
* Reads `.dcm` (DICOM) images and saves them as `.npy` (NumPy arrays).
* Saves YOLO labels as `.txt` files.

**Purpose:**
Prepare dataset for YOLO model training using DICOM images and XML annotations.

---

#### ✅ `dcmtopng.py`

**Function:**

* Reads DICOM files (`.dcm`).
* Normalizes pixel values to the 0–255 range.
* Resizes images to 512x512.
* Converts to RGB if necessary.
* Saves images as `.png` files.

**Purpose:**
Convert medical DICOM images into a general image format (PNG) for visualization or use in non-medical machine learning workflows.

---

#### ✅ `selectdatasetsandlabels.py`

**Function:**

* Compares filenames (without extension) between two folders (e.g., images and labels).
* Identifies unmatched files.
* Moves unmatched files to a separate folder for inspection or deletion.

**Purpose:**
Ensure dataset integrity by keeping only paired image-label sets and removing unmatched files.

---

#### ✅ `xmltotxt.py`

**Function:**

* Converts XML annotations to YOLO `.txt` label format.
* Uses a label mapping dictionary (e.g., `'A': 0, 'B': 1, ...`).
* Converts bounding boxes from XML to normalized YOLO format (assumes image size is 512x512).
* Saves each annotation as a text file.

**Purpose:**
Batch convert annotation files into YOLO format for model training.

---

#### ✅ `dcm.py`

**Function:**

* Reads a CSV file containing valid DICOM UIDs.
* Traverses the DICOM source directory to find files matching the UIDs.
* Verifies that a matching annotation exists for each file.
* Copies matched DICOM files into a destination folder.

**Purpose:**
Filter and retain only DICOM images that have corresponding annotation files.

---

### 🔁 **Overall Workflow**

```
[ Raw DICOM Files (.dcm) ]
          │
          ▼
   ┌──── dcm.py ─────┐
   │ Filters DICOMs  │
   └─────────────────┘
          │
          ▼
[ Valid DICOM + XML Annotations ]
          │
          ├──► data_labels.py → YOLO Labels (.txt) + Image Arrays (.npy)
          ├──► dcmtopng.py → Resized RGB Images (.png)
          └──► xmltotxt.py → Standalone YOLO Labels from XML
          
Finally:
selectdatasetsandlabels.py → Remove unpaired images or labels
```

---

### 📦 **Directory Structure Example**

```
.
├── data_labels.py
├── dcmtopng.py
├── selectdatasetsandlabels.py
├── xmltotxt.py
├── dcm.py
├── data/               # NumPy array images saved here
├── labels/             # YOLO text label files
├── datasets/           # PNG converted images
├── nolabels/           # Unpaired images or labels
├── Lung-PET-CT-Dx/     # Original DICOM dataset
└── Annotation/         # Original XML annotations
```

---

### 🧰 **Requirements**

Make sure the following Python packages are installed:

```bash
pip install pydicom numpy opencv-python Pillow pandas
```

---

### 📌 **Usage Notes**

* Customize the paths inside each script to match your local environment.
* Run the scripts in this logical order for a clean data pipeline.
* Ensure that the image dimensions are consistent (especially if using YOLO format).
* The scripts assume DICOM files contain `SOPInstanceUID` to match with XML.

---


