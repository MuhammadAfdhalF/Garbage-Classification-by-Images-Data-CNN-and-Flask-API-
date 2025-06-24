    #!/bin/bash

    # Pastikan Git LFS sudah diinisialisasi untuk repositori ini.
    # Ini akan mengaktifkan Git LFS jika belum.
    git lfs install

    # Unduh semua file yang dikelola oleh Git LFS.
    # Ini adalah langkah kunci untuk mendapatkan model Anda.
    git lfs pull

    # Jalankan aplikasi Python Anda.
    # Gunakan 'python' atau 'python3' tergantung pada versi Python yang ingin Anda gunakan.
    python3 app.py
    