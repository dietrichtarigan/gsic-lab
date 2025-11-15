# Indonesia Labor Market Intelligence Dashboard

Dashboard analitik berbasis Streamlit untuk memantau indikator pasar tenaga kerja Indonesia menggunakan data sintetis bergaya Sakernas 2020-2023.

## Struktur Proyek

```
.
├── dashboards/
│   ├── __init__.py
│   └── indonesia_labor_dashboard.py
├── data/
│   └── indonesia_labor_market.csv
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

- `streamlit_app.py` adalah entry point yang dibaca oleh Streamlit Community Cloud maupun `streamlit run`.
- `dashboards/indonesia_labor_dashboard.py` menyimpan logika utama visualisasi.
- `data/indonesia_labor_market.csv` berisi dataset sintetis untuk ditampilkan di dashboard.
- `requirements.txt` memastikan dependensi terpasang saat deploy.

## Menjalankan Secara Lokal

1. Buat dan aktifkan virtual env (opsional tetapi direkomendasikan).
2. Instal dependensi:
   ```powershell
   pip install -r requirements.txt
   ```
3. Jalankan dashboard:
   ```powershell
   streamlit run streamlit_app.py
   ```
4. Buka tautan yang muncul di terminal (`http://localhost:8501`).

## Deploy ke GitHub

1. Inisialisasi repository di folder proyek:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Buat repository baru di GitHub, lalu sambungkan remote dan dorong perubahan:
   ```powershell
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```

## Deploy ke Streamlit Community Cloud

1. Pastikan repository GitHub berisi seluruh struktur di atas.
2. Masuk ke [share.streamlit.io](https://share.streamlit.io), hubungkan akun GitHub, dan pilih repository ini.
3. Pada pengaturan aplikasi pilih:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: gunakan versi default atau sesuaikan dengan lokal.
   - **Packages**: Streamlit akan membaca `requirements.txt` secara otomatis.
4. Klik *Deploy* dan tunggu hingga build selesai. Aplikasi akan tersedia di URL publik yang dapat dibagikan.

## Pengembangan Lanjutan

- Update `requirements.txt` setiap kali menambah dependensi baru.
- Tempatkan data tambahan di folder `data/` dan gunakan `pathlib.Path` agar path relatif tetap aman.
- Bila diperlukan konfigurasi tampilan, buat file `.streamlit/config.toml`.
