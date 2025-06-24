#!/bin/bash

# Pastikan Git LFS sudah terinstal dan pull file LFS
# Ini akan memastikan model diunduh sebelum aplikasi berjalan
echo "Running git lfs pull..."
git lfs pull
echo "Git LFS pull completed."

# Pindah ke direktori tempat app.py berada, jika diperlukan.
# Karena Dockerfile menyalin isi GarbageClassification ke /app, maka app.py akan ada di /app
# Jadi, perintah berikutnya akan dijalankan dari /app.

# Lanjutkan dengan menjalankan aplikasi Flask
# Pastikan Flask dijalankan dengan host 0.0.0.0 agar bisa diakses dari luar container
# Dan gunakan port yang sesuai, misalnya dari variabel lingkungan PORT
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=${PORT:-7860}