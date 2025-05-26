from flask import Flask, request, jsonify, send_file
import os
import tempfile
from inference import remove_watermark  # <- важно: функция обработки из original repo

app = Flask(__name__)

@app.route("/")
def home():
    return "Video Watermark Remover API is running!"

@app.route("/remove_watermark", methods=["POST"])
def remove():
    if 'video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video_file = request.files['video']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as input_temp:
        video_path = input_temp.name
        video_file.save(video_path)

    # Путь для результата
    output_path = video_path.replace(".mp4", "_no_watermark.mp4")

    try:
        remove_watermark(video_path, output_path)  # функция из original repo
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
