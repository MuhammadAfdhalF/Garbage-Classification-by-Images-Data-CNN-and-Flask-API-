# Gunakan image dasar Python
# Sesuaikan versi Python jika Anda menggunakan versi tertentu (misal python:3.9-slim-buster)
FROM python:3.9-slim-buster

# Instal Git LFS
# Ini akan memastikan Git LFS client tersedia di dalam container
RUN apt-get update && apt-get install -y git-lfs && rm -rf /var/lib/apt/lists/*

# Set direktori kerja di dalam container.
# Ini harus sama dengan direktori build di Railway (GarbageClassification/)
WORKDIR /app/GarbageClassification

# Salin semua file dari repositori lokal Anda ke direktori kerja di dalam container.
# Perhatikan titik pertama (.) yang berarti "direktori saat ini di host" (yaitu root repositori Anda)
# dan titik kedua (.) yang berarti "direktori kerja di container"
# Ini akan menyalin seluruh isi folder GarbageClassification/ dan juga .git/
COPY . /app/GarbageClassification

# Karena kita menyalin seluruh repositori termasuk .git/,
# kita perlu memastikan Git LFS mengunduh file sebenarnya
# LFS install akan mengaktifkan filtering LFS
# LFS pull akan mengunduh file besar yang ditunjuk oleh pointer LFS
RUN git lfs install --local && git lfs pull

# Instal dependensi Python
# Pastikan requirements.txt ada di dalam GarbageClassification/
RUN pip install --no-cache-dir -r requirements.txt

# Atur variabel lingkungan yang diperlukan oleh Flask
# Pastikan app.py adalah file utama Flask Anda
ENV FLASK_APP=app.py

# Ekspos port yang akan didengarkan aplikasi Flask Anda
# Railway akan menggunakan ini untuk merutekan traffic
EXPOSE 5000

# Perintah untuk menjalankan aplikasi Flask Anda
# Ini akan dieksekusi saat container dijalankan
CMD ["python3", "app.py"]
