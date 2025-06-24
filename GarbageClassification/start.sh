#!/bin/bash

# Ini akan menginstal Git LFS jika belum ada.
# Beberapa base image sudah memiliki 'git-lfs', jadi baris ini mungkin tidak selalu diperlukan,
# tetapi aman untuk disertakan jika Nixpacks belum menyediakannya secara default.
apt-get update && apt-get install -y git-lfs

# Menginisialisasi Git LFS untuk repositori ini.
# Ini akan memastikan perintah 'git lfs pull' dapat berjalan.
git lfs install

# Mengunduh semua file besar yang dikelola oleh Git LFS.
# Ini adalah langkah KRUSIAL untuk mendapatkan final_model_33.h5 yang sebenarnya.
git lfs pull

# Jalankan aplikasi Python Anda.
# Gunakan 'python' atau 'python3' tergantung pada versi Python yang ingin Anda gunakan
# dan bagaimana lingkungan Railway mengaturnya. 'python3' umumnya lebih spesifik dan aman.
python3 app.py
