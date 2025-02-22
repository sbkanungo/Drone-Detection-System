from ultralytics import YOLO

# Load a YOLOv8 model (pretrained on COCO)
model = YOLO("yolov8n.pt")  # You can also use yolov8s.pt, yolov8m.pt, etc.

# Train model for 20 epochsmodel.train(data="C:/dronetrack/Drone Detection.v1i.yolov8/data.yaml", epochs=50, patience=5, batch=8, imgsz=640)
model.train(data="C:/dronetrack/Drone Detection.v1i.yolov8/data.yaml", epochs=50, patience=5, batch=8, imgsz=640)

