# models/video_tracker.py
import cv2
from ultralytics import YOLO
import pandas as pd
import os

# Загружаем модель один раз при старте
model = YOLO("yolov8n.pt")

def analyze_video(video_path, output_csv="data/logs.csv"):
    # Создаём папку data, если её нет
    os.makedirs("data", exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Не удалось открыть видео: {video_path}")

    logs = []
    frame_id = 0

    print("Анализ видео начат…")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        break

        # BoT-SORT включён по умолчанию в новых версиях Ultralytics (8.3.233 у тебя стоит)
        # поэтому просто указываем persist=True и classes=[0] (люди)
        results = model.track(
            source=frame,
            persist=True,           # сохранять ID между кадрами
            tracker="botsort.yaml",  # можно оставить, даже если файла нет — Ultralytics использует встроенный
            classes=[0],            # только класс "person"
            verbose=False
        )

        boxes = results[0].boxes
        if boxes.id is not None:
            for box, track_id in zip(boxes.xyxy, boxes.id):
                x1, y1, x2, y2 = map(int, box)
                tid = int(track_id)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                logs.append({
                    "frame": frame_id,
                    "person_id": tid,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "center_x": center_x,
                    "center_y": center_y
                })

        frame_id += 1

    cap.release()

    # Сохраняем результат
    df = pd.DataFrame(logs)
    if not df.empty:
        df.to_csv(output_csv, index=False)
        print(f"Готово! Уникальных людей: {df['person_id'].nunique()}")
    else:
        print("Люди не обнаружены")
        df = pd.DataFrame(columns=["frame", "person_id", "center_x", "center_y"])

    return df