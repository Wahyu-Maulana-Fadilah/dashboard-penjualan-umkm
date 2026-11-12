# Dashboard Penjualan UMKM

Tugas Statistika dan Probabilitas 1 (Kelas A) — dashboard interaktif dengan Streamlit.

## Pertanyaan analisis
1. Produk dan kategori apa yang menyumbang omzet terbesar, dan bagaimana tren penjualannya dari waktu ke waktu?
2. Channel penjualan mana yang paling besar kontribusinya terhadap omzet?

## Dataset
- Nama     : Dataset_Penjualan_UMKM_1000 (1.000 transaksi, 1 Jan – 9 Apr 2024)
- Sumber   : **https://www.kaggle.com/datasets/hermawansaputro1/dataset-penjualan**
- Kolom    : Invoice_ID, Tanggal, Nama_Produk, Kategori, Jumlah_Terjual, Harga_Satuan, Total_Penjualan, Metode_Pembayaran, Channel_Penjualan, Nama_Pelanggan, Wilayah
- Numerik  : Jumlah_Terjual, Harga_Satuan, Total_Penjualan
- Kategori : Kategori, Nama_Produk, Channel_Penjualan, Metode_Pembayaran, Wilayah

### Data wrangling (`data_cleaning.py`)
1. Memeriksa tipe data, missing value (0), dan duplikat (0).
2. Merapikan spasi pada kolom teks.
3. Mengubah `Tanggal` ke datetime.
4. Harga_Satuan distandarkan satu harga tetap per produk (sebelumnya acak per baris), lalu `Total_Penjualan = Jumlah_Terjual x Harga_Satuan`.
5. Hasil bersih disimpan ke `data.csv`.

## Fitur dashboard
- Filter di sidebar: periode transaksi dan kategori produk.
- Ringkasan angka & statistik deskriptif (`st.metric`): total omzet, jumlah transaksi, total unit terjual, serta mean, median, simpangan baku (std), dan IQR nilai transaksi.
- Visualisasi: line chart tren penjualan harian, bar chart omzet per kategori, donut chart porsi channel penjualan, dan horizontal bar chart 5 produk terlaris.
- Setiap grafik disertai penjelasan "Yang terlihat" dan "Artinya".

## Struktur folder
```
dashboard/
  dashboard.py       kode utama Streamlit
  data.csv           data bersih
  data_cleaning.py   tahap wrangling (Excel -> CSV)
  requirements.txt
  README.md
```
