from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model(source="C:/Users/hui21/Downloads/stop_sign_test_vid.mp4", 
                show=True, conf=0.4, save=True, save_dir="C:/Users/hui21/Downloads",
                classes=[11, 9])
