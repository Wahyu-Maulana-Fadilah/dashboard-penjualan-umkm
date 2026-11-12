"""
Tahap data wrangling: membaca Excel -> memeriksa -> membersihkan -> menyimpan data.csv
Jalankan sekali:  python data_cleaning.py
"""
from pathlib import Path
import pandas as pd

SRC = Path(__file__).parent / "Dataset_Penjualan_UMKM_1000_fixed.xlsx"
OUT = Path(__file__).parent / "data.csv"

df = pd.read_excel(SRC)
print(f"Baris x kolom awal : {df.shape}")
print("\nTipe data:\n", df.dtypes.to_string())
print("\nMissing value per kolom:\n", df.isna().sum().to_string())
print(f"\nBaris duplikat      : {df.duplicated().sum()}")
print(f"Invoice_ID duplikat : {df['Invoice_ID'].duplicated().sum()}")

# 1. Rapikan nama kolom & spasi berlebih pada teks
df.columns = df.columns.str.strip()
for col in ["Invoice_ID", "Nama_Produk", "Kategori", "Metode_Pembayaran", "Channel_Penjualan", "Nama_Pelanggan", "Wilayah"]:
    df[col] = df[col].astype(str).str.strip()

# 2. Kolom tanggal -> datetime
df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

# 3. Buang duplikat dan baris tanpa tanggal / angka
df = df.drop_duplicates(subset="Invoice_ID")
df = df.dropna(subset=["Tanggal", "Jumlah_Terjual", "Harga_Satuan"])

# 4. Pastikan Total_Penjualan konsisten = Jumlah x Harga
df["Total_Penjualan"] = df["Jumlah_Terjual"] * df["Harga_Satuan"]

# 5. Urutkan berdasarkan waktu & simpan
df = df.sort_values(["Tanggal", "Invoice_ID"]).reset_index(drop=True)
df.to_csv(OUT, index=False, date_format="%Y-%m-%d")

print(f"\nSelesai. {len(df)} baris disimpan ke {OUT.name}")
print(f"Rentang tanggal: {df['Tanggal'].min().date()} s.d. {df['Tanggal'].max().date()}")
