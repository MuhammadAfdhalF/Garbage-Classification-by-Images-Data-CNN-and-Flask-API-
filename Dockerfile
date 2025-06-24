# Gunakan base image Python yang sesuai. Python 3.9 adalah versi yang stabil.
FROM python:3.9-slim-buster

# Perbarui daftar paket dan instal git-lfs.
# Ini penting jika model Anda di-host menggunakan Git LFS.
RUN apt-get update && \
    apt-get install -y --no-install-recommends git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Set working directory di dalam container
WORKDIR /app

# Copy requirements.txt dari root host ke root container dan instal dependencies
# Pastikan requirements.txt ada di root folder repository Anda.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy sisa kode aplikasi dari subfolder GarbageClassification ke dalam root container
# Ini akan menyalin app.py, templates/, static/, dan final_model_33.h5 langsung ke /app
COPY GarbageClassification/ .

# Copy folder ss (jika ada aset statis atau gambar lain yang diperlukan oleh aplikasi)
# Pastikan folder ss ada di root folder repository Anda.
COPY ss/ ./ss/

# Copy file start.sh dari root host ke root container
# Pastikan start.sh ada di root folder repository Anda.
COPY start.sh .

# Berikan izin eksekusi pada start.sh
RUN chmod +x start.sh

# Expose port yang digunakan aplikasi kamu (7860 adalah standar untuk HF Spaces)
# Pastikan ini sesuai dengan port yang di-listen oleh aplikasi Python kamu di app.py / start.sh
EXPOSE 7860

# Command untuk menjalankan aplikasi.
# start.sh akan menjalankan app.py yang sekarang berada langsung di /app/app.py
CMD ["./start.sh"]
