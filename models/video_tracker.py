import cv2
from ultralytics import YOLO
import pandas as pd
import yaml  # Для конфига трекера

# Конфиг для BoT-SORT (сохраните как botsort.yaml в configs/)
tracker_config = {
    'tracker_type': 'botsort',
    'reid_weights': 'osnet_x0_25_msmt17.pt'  # Для re-ID
}
with open('configs/botsort.yaml', 'w') as f:
    yaml.dump(tracker_config, f)

model = YOLO('yolov8n.pt')  # Nano для скорости

def analyze_video(video_path, output_csv='data/logs.csv'):
    cap = cv2.VideoCapture(video_path)
    logs = []
    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        results = model.track(frame, persist=True, tracker='configs/botsort.yaml', classes=0)  # Люди, persistent ID
        for r in results[0].boxes:
            if r.id is not None:
                bbox = r.xyxy[0].cpu().numpy().tolist()
                logs.append({'frame': frame_id, 'id': int(r.id), 'bbox': bbox})
        frame_id += 1
    cap.release()

    df = pd.DataFrame(logs)
    df.to_csv(output_csv, index=False)
    return df