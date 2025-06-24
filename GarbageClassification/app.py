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


    app = Flask(__name__)

    # Path folder untuk menyimpan gambar upload
    UPLOAD_FOLDER = 'static/uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Load model
    model = tf.keras.models.load_model("final_model_33.h5")
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
            print("🖼️ Gambar disimpan di:", filepath)

            return render_template('picture.html', prediction=class_name, image_url=filepath)

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

            os.remove(filepath)
            return jsonify({'prediction': class_name})

        except Exception as e:
            print(f"Error processing live image: {e}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Failed to process live image: {str(e)}'}), 500

    if __name__ == '__main__':
        # Dapatkan port dari variabel lingkungan Railway
        port = int(os.environ.get('PORT', 5000)) # 5000 sebagai fallback untuk lokal
        app.run(debug=False, host='0.0.0.0', port=port)