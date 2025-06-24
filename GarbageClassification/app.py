import os
from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
from werkzeug.utils import secure_filename
import uuid

# --- KONFIGURASI TENSORFLOW UNTUK LINGKUNGAN CPU ---
# Ini akan mencegah TensorFlow mencari GPU dan menekan warning terkait CUDA/cuDNN
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # Memberitahu TensorFlow untuk tidak melihat GPU
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # Menekan warning specific dari TensorFlow (seperti di log Anda)

# Anda juga bisa menambahkan ini jika ada warning spesifik lain (opsional, jika masih banyak warning):
# import logging
# tf.get_logger().setLevel(logging.ERROR)
# --- AKHIR KONFIGURASI TENSORFLOW ---

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Path folder untuk menyimpan gambar upload
# Pastikan folder static/uploads ada di dalam GarbageClassification/
UPLOAD_FOLDER_RELATIVE = 'static/uploads'
UPLOAD_FOLDER_ABSOLUTE = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER_RELATIVE)
os.makedirs(UPLOAD_FOLDER_ABSOLUTE, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_ABSOLUTE

# Load model
# Pastikan final_model_33.h5 ada di dalam folder yang sama dengan app.py
MODEL_PATH = os.path.join(os.path.dirname(__file__), "final_model_33.h5")
model = tf.keras.models.load_model(MODEL_PATH)
target_size = (224, 224)

# Mapping output ke nama label
waste_labels = {
    1: 'glass',
    2: 'metal',
    3: 'paper',
    4: 'plastic',
    5: 'trash'
}

# === ROUTES ===

@app.route('/')
def index():
    return render_template('index.html', prediction=None, image_url=None)

@app.route('/picture')
def picture():
    return render_template('picture.html')

@app.route('/live_camera')
def live_camera():
    return render_template('live_camera.html')

# Endpoint untuk form upload di picture.html
@app.route('/predict', methods=['POST'])
def predict_static_image():
    if 'image' not in request.files:
        print("⛔ Tidak ada file dengan nama 'image' di form.")
        return render_template('picture.html', prediction="No image uploaded", image_url=None)

    file = request.files['image']
    if file.filename == '':
        print("⛔ File yang diupload tidak memiliki nama.")
        return render_template('picture.html', prediction="No selected image", image_url=None)

    # Validasi ekstensi file
    allowed_extensions = {'jpg', 'jpeg', 'png', 'bmp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        print("⛔ Ekstensi file tidak valid:", file.filename)
        return render_template('picture.html', prediction="Invalid file type", image_url=None)

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

        # Prediksi menggunakan model
        pred = model.predict(img_array)[0]
        class_index = np.argmax(pred) + 1
        class_name = waste_labels.get(class_index, "Unknown")

        print("✅ Prediksi berhasil:", class_name)
        # Untuk URL gambar yang ditampilkan di HTML, gunakan jalur relatif dari root static
        display_image_url = os.path.join(UPLOAD_FOLDER_RELATIVE, filename).replace('\\', '/') # Mengganti backslash untuk URL
        print("🖼️ Gambar disimpan di:", filepath)


        return render_template('picture.html', prediction=class_name, image_url=display_image_url)

    except Exception as e:
        print(f"❌ Error saat memproses gambar: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return render_template('picture.html', prediction=f"Error processing image: {str(e)}", image_url=None)


# Endpoint untuk live camera API (return JSON)
@app.route('/live_predict', methods=['POST'])
def live_predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    file_ext = os.path.splitext(secure_filename(file.filename))[1]
    unique_filename = str(uuid.uuid4()) + file_ext
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)

    try:
        img = Image.open(filepath).convert("RGB")
        img = img.resize(target_size)
        img_array = np.array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        pred = model.predict(img_array)[0]
        class_index = np.argmax(pred) + 1
        class_name = waste_labels.get(class_index, "Unknown")

        os.remove(filepath) # Hapus gambar setelah diproses
        return jsonify({'prediction': class_name})

    except Exception as e:
        print(f"Error processing live image: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'Failed to process live image: {str(e)}'}), 500

if __name__ == '__main__':
    # Dapatkan port dari variabel lingkungan, default ke 7860 untuk Hugging Face Spaces
    port = int(os.environ.get('PORT', 7860)) 
    app.run(debug=False, host='0.0.0.0', port=port)
