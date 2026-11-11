# Proyek Analisis Data: Bike Sharing Dataset

Proyek analisis data penyewaan sepeda **Capital Bikeshare (Washington D.C.)** periode 2011–2012.
Analisis mencakup seluruh tahapan: pertanyaan bisnis SMART, data wrangling, EDA, visualisasi,
kesimpulan, dan rekomendasi action item, serta dashboard interaktif menggunakan Streamlit.

**Nama:** Atikah Fahira

## Pertanyaan Bisnis
1. Bagaimana perbedaan rata-rata penyewaan sepeda antara musim (Spring, Summer, Fall, Winter) selama periode 2011–2012?
2. Bagaimana perbandingan persentase penyewaan pengguna casual dan registered terhadap total penyewaan pada hari kerja dan hari non-kerja (akhir pekan dan hari libur) selama periode 2011–2012 untuk mendukung penyusunan strategi pemasaran berdasarkan segmen pengguna?

## Struktur Direktori
```
submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   └── day.csv
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Menjalankan Dashboard
Dari folder utama proyek (`submission`):
```
streamlit run dashboard/dashboard.py
```
Dashboard akan terbuka di browser pada `http://localhost:8501`.

## Fitur Dashboard
- Filter rentang tanggal, musim, dan jenis hari pada sidebar
- Ringkasan metrik: total penyewaan, rata-rata harian, persentase pengguna registered dan casual
- Pertanyaan 1: rata-rata dan distribusi penyewaan per musim, serta tren rata-rata per bulan
- Pertanyaan 2: komposisi pengguna casual vs registered pada hari kerja dan non-kerja
- Analisis lanjutan: distribusi tingkat permintaan (Rendah/Sedang/Tinggi) per musim
- Kesimpulan dan rekomendasi action item

## Ringkasan Hasil
- Musim **Fall** memiliki rata-rata penyewaan tertinggi (±5.644 per hari), sedangkan **Spring** terendah (±2.604 per hari).
- Pengguna **Registered** mendominasi hari kerja (86,77%), sedangkan kontribusi **Casual** naik menjadi 31,66% pada hari non-kerja.

## Sumber Data
Bike Sharing Dataset (`day.csv`), Capital Bikeshare, Washington D.C., 2011–2012.
