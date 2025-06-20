from flask import Flask, render_template, request, jsonify # Import jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
import os
from werkzeug.utils import secure_filename
import uuid # Import uuid for unique filenames

app = Flask(__name__)

# Path folder untuk menyimpan gambar upload
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load model
model = tf.keras.models.load_model("final_model_33.h5")

# Ukuran input yang sesuai untuk VGG16
target_size = (224, 224)

# Mapping output ke nama label
waste_labels = {
    1: 'glass',
    2: 'metal',
    3: 'paper',
    4: 'plastic',
    5: 'trash'
}

@app.route('/')
def index():
    # Pastikan prediction dan image_url diinisialisasi untuk tampilan awal
    return render_template('index.html', prediction=None, image_url=None)

# --- Endpoint untuk Unggahan Gambar Statis (dari form HTML) ---
@app.route('/predict', methods=['POST'])
def predict_static_image():
    if 'image' not in request.files:
        return render_template('index.html', prediction="No image uploaded", image_url=None)

    file = request.files['image']

    if file.filename == '':
        return render_template('index.html', prediction="No selected image", image_url=None)

    # Nama file untuk unggahan statis bisa tetap sama, tidak perlu unik per detik
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Proses gambar
        img = Image.open(filepath).convert("RGB")
        img = img.resize(target_size)
        img_array = np.array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Prediksi
        pred = model.predict(img_array)[0]
        class_index = np.argmax(pred) + 1
        class_name = waste_labels.get(class_index, "Unknown")

        # Opsional: Jika ingin menghapus file setelah diproses untuk upload biasa juga
        # os.remove(filepath)

        return render_template('index.html', prediction=class_name, image_url=filepath)

    except Exception as e:
        print(f"Error processing uploaded image: {e}")
        # Hapus file jika terjadi error saat pemrosesan
        if os.path.exists(filepath):
            os.remove(filepath)
        return render_template('index.html', prediction=f"Error processing image: {str(e)}", image_url=None)

# --- Endpoint Baru untuk Live Camera (selalu mengembalikan JSON) ---
@app.route('/live_predict', methods=['POST'])
def live_predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    # Dapatkan ekstensi file asli
    file_ext = os.path.splitext(secure_filename(file.filename))[1]

    # Generate nama file unik menggunakan UUID untuk menghindari race condition
    unique_filename = str(uuid.uuid4()) + file_ext
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    file.save(filepath) # Simpan frame dengan nama unik

    try:
        # Proses gambar
        img = Image.open(filepath).convert("RGB")
        img = img.resize(target_size)
        img_array = np.array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Prediksi
        pred = model.predict(img_array)[0]
        class_index = np.argmax(pred) + 1
        class_name = waste_labels.get(class_index, "Unknown")

        # Hapus file setelah diproses untuk menghindari penumpukan
        os.remove(filepath)

        return jsonify({'prediction': class_name}) # Selalu kembalikan JSON

    except Exception as e:
        print(f"Error processing live image: {e}")
        # Pastikan file unik juga dihapus jika terjadi error
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'Failed to process live image: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)