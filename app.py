from flask import Flask, request, jsonify, send_file
import os
import tempfile
from inference import remove_watermark

app = Flask(__name__)

@app.route("/")
def home():
    return "Video Watermark Remover API is running!"

@app.route("/remove_watermark", methods=["POST"])
def remove():
    if 'video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    # Чтение координат из формы
    try:
        x = int(request.form.get("x", 0))
        y = int(request.form.get("y", 0))
        w = int(request.form.get("w", 100))
