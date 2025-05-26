from moviepy.editor import VideoFileClip
import cv2
import numpy as np
import os
import tempfile

def remove_watermark(input_path, output_path):
    # Сначала извлечём аудио
    video = VideoFileClip(input_path)
    audio = video.audio

    # Сохраним видео без звука во временный файл
    temp_no_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    video.without_audio().write_videofile(temp_no_audio, codec='libx264', audio=False)

    # Откроем с помощью OpenCV
    cap = cv2.VideoCapture(temp_no_audio)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_processed = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    out = cv2.VideoWriter(temp_processed, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Тут размытие логотипа — координаты подбери под своё видео
        x, y, w, h = 50, 50, 100, 50
        roi = frame[y:y+h, x:x+w]
        roi = cv2.GaussianBlur(roi, (15, 15), 0)
        frame[y:y+h, x:x+w] = roi

        out.write(frame)

    cap.release()
    out.release()

    # Теперь вернём звук обратно
    final = VideoFileClip(temp_processed).set_audio(audio)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Очистка временных файлов
    os.remove(temp_no_audio)
    os.remove(temp_processed)
