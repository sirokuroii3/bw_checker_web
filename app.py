from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return "ファイルが見つかりません", 400
    file = request.files['image']
    if file.filename == '':
        return "ファイルが選択されていません", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return "画像の読み込みに失敗しました", 400

    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    total_pixels = binary.size
    white_pixels = np.count_nonzero(binary == 255)
    black_pixels = total_pixels - white_pixels
    white_ratio = white_pixels / total_pixels * 100
    black_ratio = black_pixels / total_pixels * 100

    result = {
        'white_ratio': f"{white_ratio:.2f}%",
        'black_ratio': f"{black_ratio:.2f}%"
    }

    return render_template('result.html', result=result, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
