from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import os
import stepic
from datetime import datetime as dt

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return redirect(url_for('stego'))

@app.route('/stego')
def stego():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if request.method == "POST":
        message = request.form['message']
        image = request.files['image']

        save_path = os.path.join(UPLOAD_FOLDER, 'original.png')
        image.save(save_path)

        original_image = Image.open(save_path)
        encoded_image = stepic.encode(original_image, message.encode())

        # Create a unique filename with timestamp
        filename = f'{dt.now().strftime("%Y%m%d_%H%M%S")}.png'
        encoded_path = os.path.join(UPLOAD_FOLDER, filename)
        encoded_image.save(encoded_path)

        return render_template("result.html", encoded=True, filename=filename)

@app.route('/return_encoded/<filename>')
def return_encoded(filename):
    encoded_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(encoded_path):
        return send_file(encoded_path, mimetype='image/png')
    else:
        return "File not found", 404

@app.route('/decode', methods=['POST'])
def decode():
    if request.method == "POST":
        image = request.files['image']
        save_path = os.path.join(UPLOAD_FOLDER, 'to_decode.png')
        image.save(save_path)

        image = Image.open(save_path)
        message = stepic.decode(image)

        return render_template("result.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
