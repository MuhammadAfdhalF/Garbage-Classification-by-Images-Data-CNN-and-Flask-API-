# Gunakan base image Python yang sesuai. Sesuaikan versi Python jika diperlukan.
# Disarankan menggunakan versi spesifik yang kamu pakai (misal: python:3.9-slim)
FROM python:3.9-slim

# --- BAGIAN BARU: Instalasi Git LFS ---
# Perbarui daftar paket dan instal git-lfs
RUN apt-get update && \
    apt-get install -y --no-install-recommends git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*
# -----------------------------------

# Set working directory di dalam container
WORKDIR /app

# Copy requirements.txt dan install dependencies terlebih dahulu
# Ini memanfaatkan Docker cache layer jika requirements.txt tidak berubah
COPY GarbageClassification/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy sisa kode aplikasi dari subfolder GarbageClassification ke dalam container
COPY GarbageClassification/ .

# Copy folder ss (jika ada aset statis atau gambar yang diperlukan oleh aplikasi)
COPY ss/ ./ss/

# Copy file start.sh
COPY GarbageClassification/start.sh .

# Berikan izin eksekusi pada start.sh
RUN chmod +x start.sh

# Expose port yang digunakan aplikasi kamu (biasanya 5000 untuk Flask, atau 7860 untuk HF Spaces)
# Penting: Pastikan ini sesuai dengan port yang di-listen oleh aplikasi Python kamu di app.py / start.sh
EXPOSE 7860

# Command untuk menjalankan aplikasi.
# Pastikan start.sh menjalankan app.py dengan benar.
CMD ["./start.sh"]