FROM python:3.10-slim

# Установка системных библиотек, включая libGL
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 libgl1-mesa-glx && \
    apt-get clean

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Открываем нужный порт
EXPOSE 7860

# Запуск Python приложения
CMD ["python", "app.py"]
