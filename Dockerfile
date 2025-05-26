FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 libgl1-mesa-glx && \
    apt-get clean

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Указание порта
EXPOSE 7860

# Запуск приложения
CMD ["python", "app.py"]
