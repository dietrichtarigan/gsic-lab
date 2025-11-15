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
- `dashboards/indonesia_labor_dashboard.py` menyimpan logika utama visualisasi yang kini terbagi dalam beberapa modul intelijen (macro overview, supply-demand, benchmarking, early warning, policy tracker, citizen tools).
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

### Modul Dashboard

Dashboard kini terdiri dari sembilan tab utama:

1. **Talent Control Tower**: Bar chart race GTCI, gauge pilar, serta simulator kebijakan berbasis skenario untuk mengejar kompetisi talent ASEAN.
2. **Digital Readiness Map**: Peta pydeck yang menggabungkan IMDI & literasi digital, analitik mismatch wired-vs-skilled, serta radar diagnostik provinsi.
3. **Real-Time Demand**: Tracker lowongan vs PHK, heatmap skill genome, top emerging skills, mismatch kalkulator, dan scorecard Decent Work vs ASEAN.
4. **Macro Overview**: KPI nasional, tren TPT/TPAK, dan explorer provinsi.
5. **Supply-Demand & Skill Gap**: Indeks supply-demand, gap provinsi, heatmap struktur sektor, dan radar skill.
6. **Regional Benchmarking**: Komparasi KPI antar-provinsi, trajektori historis, dan scorecard melawan rata-rata nasional.
7. **Early Warning System**: Deteksi lonjakan TPT, pulse indikator leading, dan proxy indeks lowongan SiapKerja.
8. **Policy Lab**: Tracker RPJMN dengan gauge, plus benchmark ASEAN/G20.
9. **Pelatihan & Citizen Tools**: Direktori BLK dengan unduhan CSV dan kalkulator estimasi gaji sektoral.

## Pengembangan Lanjutan

- Update `requirements.txt` setiap kali menambah dependensi baru.
- Tempatkan data tambahan di folder `data/` dan gunakan `pathlib.Path` agar path relatif tetap aman.
- Bila diperlukan konfigurasi tampilan, buat file `.streamlit/config.toml`.
