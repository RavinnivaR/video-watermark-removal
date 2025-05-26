import cv2
import numpy as np

def remove_watermark(input_path, output_path):
    # Загрузка видео
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Пример простого удаления водяного знака: размытие области
        # Замените координаты (x, y, w, h) на область вашего водяного знака
        x, y, w, h = 50, 50, 100, 50
        roi = frame[y:y+h, x:x+w]
        roi = cv2.GaussianBlur(roi, (15, 15), 0)
        frame[y:y+h, x:x+w] = roi

        out.write(frame)

    cap.release()
    out.release()
