import yaml
import os
import kagglehub

# Download dataset
path = kagglehub.dataset_download("anggadwisunarto/potholes-detection-yolov8")

print("Path to dataset files:", path)

# Writable path for data.yaml
writable_yaml_path = os.path.join("./", "data.yaml")

# Check if data.yaml exists at writable path
if os.path.exists(writable_yaml_path):
    with open(writable_yaml_path, 'r') as f:
        data = yaml.safe_load(f)
else:
    # Create a new dictionary if not existing
    data = {'names': ['pothole'], 'nc': 1}

# Update the correct paths
data['path'] = path           # The root of the dataset
data['train'] = os.path.join(path, 'train/images')  # Absolute path relative to 'path'
data['val'] = os.path.join(path, 'valid/images')    # Absolute path relative to 'path'
data['test'] = os.path.join(path, 'test/images')    # Absolute path relative to 'path'

# Write back to the writable path
with open(writable_yaml_path, 'w') as f:
    yaml.dump(data, f)

print(f"✅ Fixed YAML! Now pointing to: {path}")
print(f"Saved data.yaml to: {writable_yaml_path}")

from ultralytics import YOLO

# Load a pretrained model (replace with your model if different)
model = YOLO('yolov8n.pt')  # or your chosen model

# Train the model
model.train(data='./data.yaml', epochs=5, imgsz=416, batch=2, device='cpu')
