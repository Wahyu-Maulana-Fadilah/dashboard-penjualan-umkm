"""
Dashboard Penjualan UMKM
Jalankan: streamlit run dashboard.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi halaman dasar
st.set_page_config(page_title="Dashboard Penjualan UMKM", layout="wide")

# ----------------------------------------------------------------------------
# 1. Load Data (dengan @st.cache_data)
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", parse_dates=["Tanggal"])
    df["Total_Penjualan"] = df["Jumlah_Terjual"] * df["Harga_Satuan"]
    return df

try:
    df_all = load_data()
except FileNotFoundError:
    st.error("File data.csv tidak ditemukan. Pastikan data.csv berada dalam satu folder dengan dashboard.py")
    st.stop()

# ----------------------------------------------------------------------------
# 2. Sidebar Filter (Hanya Periode & Kategori)
# ----------------------------------------------------------------------------
st.sidebar.header("Filter Data")

min_tgl = df_all["Tanggal"].min().date()
max_tgl = df_all["Tanggal"].max().date()
rentang = st.sidebar.date_input("Periode Transaksi", value=(min_tgl, max_tgl), min_value=min_tgl, max_value=max_tgl)

kategori_list = sorted(df_all["Kategori"].unique())
kategori_pilih = st.sidebar.multiselect("Kategori Produk", options=kategori_list, default=kategori_list)

# Validasi input tanggal
if len(rentang) != 2:
    st.warning("Silakan pilih tanggal mulai dan tanggal akhir pada filter Periode.")
    st.stop()

start_date, end_date = pd.Timestamp(rentang[0]), pd.Timestamp(rentang[1])

# Terapkan filter
df = df_all[
    (df_all["Tanggal"] >= start_date) &
    (df_all["Tanggal"] <= end_date) &
    (df_all["Kategori"].isin(kategori_pilih))
]

if df.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

# ----------------------------------------------------------------------------
# 3. Judul Utama (Murni Dashboard Penjualan UMKM)
# ----------------------------------------------------------------------------
st.title("Dashboard Penjualan UMKM")
st.caption(f"Menampilkan {len(df):,} transaksi dari total {len(df_all):,} transaksi.")
st.divider()

# ----------------------------------------------------------------------------
# 4. Ringkasan Angka & Statistik Deskriptif (st.metric)
# ----------------------------------------------------------------------------
# Baris 1: Ringkasan Penjualan Utama
col1, col2, col3 = st.columns(3)
col1.metric("Total Omzet", f"Rp {df['Total_Penjualan'].sum():,.0f}")
col2.metric("Jumlah Transaksi", f"{len(df):,} trx")
col3.metric("Total Unit Terjual", f"{df['Jumlah_Terjual'].sum():,} unit")

st.write("")


# ----------------------------------------------------------------------------
# 5. Visualisasi & Penjelasan Singkat (4 Grafik Berbeda)
# ----------------------------------------------------------------------------

# --- Grafik 1: Tren Penjualan (Line Chart) ---
st.subheader("Tren Penjualan Harian")
tren = df.groupby("Tanggal")["Total_Penjualan"].sum().reset_index()
fig_tren = px.line(
    tren, x="Tanggal", y="Total_Penjualan",
    labels={"Tanggal": "Tanggal", "Total_Penjualan": "Total Omzet (Rp)"},
    markers=True
)
st.plotly_chart(fig_tren, use_container_width=True)
st.info(
    f"**Yang terlihat:** Omzet harian tertinggi mencapai Rp {tren['Total_Penjualan'].max():,.0f} "
    f"dan terendah Rp {tren['Total_Penjualan'].min():,.0f}.\n\n"
    "**Artinya:** Fluktuasi harian menunjukkan adanya hari-hari tertentu dengan lonjakan pembelian "
    "yang dapat dimanfaatkan untuk penjadwalan promo."
)

st.divider()

c1, c2 = st.columns(2)

with c1:
    # --- Grafik 2: Omzet per Kategori (Bar Chart) ---
    st.subheader("Omzet per Kategori")
    kat = df.groupby("Kategori")["Total_Penjualan"].sum().reset_index().sort_values("Total_Penjualan", ascending=False)
    fig_kat = px.bar(
        kat, x="Kategori", y="Total_Penjualan", color="Kategori",
        labels={"Kategori": "Kategori", "Total_Penjualan": "Total Omzet (Rp)"}
    )
    st.plotly_chart(fig_kat, use_container_width=True)
    st.info(
        f"**Yang terlihat:** Kategori **{kat.iloc[0]['Kategori']}** menyumbang omzet terbesar "
        f"(Rp {kat.iloc[0]['Total_Penjualan']:,.0f}).\n\n"
        "**Artinya:** Kategori teratas merupakan penopang utama pendapatan UMKM sehingga stoknya harus diprioritaskan."
    )

with c2:
    # --- Grafik 3: Porsi Channel Penjualan (Pie / Donut Chart) ---
    st.subheader("Porsi Channel Penjualan")
    ch = df.groupby("Channel_Penjualan")["Total_Penjualan"].sum().reset_index()
    fig_ch = px.pie(
        ch, names="Channel_Penjualan", values="Total_Penjualan", hole=0.4
    )
    st.plotly_chart(fig_ch, use_container_width=True)
    top_ch = ch.sort_values("Total_Penjualan", ascending=False).iloc[0]
    st.info(
        f"**Yang terlihat:** Saluran **{top_ch['Channel_Penjualan']}** mendominasi penjualan "
        f"dengan nilai Rp {top_ch['Total_Penjualan']:,.0f}.\n\n"
        "**Artinya:** Fokus promosi digital atau operasional sangat efektif jika diarahkan pada channel utama ini."
    )

st.divider()

# --- Grafik 4: Top 5 Produk Terlaris (Horizontal Bar Chart) ---
st.subheader("5 Produk dengan Omzet Tertinggi")
top_prod = df.groupby("Nama_Produk")["Total_Penjualan"].sum().reset_index().sort_values("Total_Penjualan", ascending=True).tail(5)
fig_prod = px.bar(
    top_prod, x="Total_Penjualan", y="Nama_Produk", orientation="h",
    labels={"Total_Penjualan": "Total Omzet (Rp)", "Nama_Produk": "Nama Produk"}
)
st.plotly_chart(fig_prod, use_container_width=True)
st.info(
    f"**Yang terlihat:** Produk **{top_prod.iloc[-1]['Nama_Produk']}** menempati posisi pertama omzet tertinggi.\n\n"
    "**Artinya:** Produk unggulan ini memiliki permintaan paling kuat dan dapat dijadikan paket bundling dengan produk lain."
)

st.divider()
# Baris 2: Statistik Deskriptif Nilai Transaksi (Mean, Median, Std, IQR)
nilai = df["Total_Penjualan"]
iqr = nilai.quantile(0.75) - nilai.quantile(0.25)

s1, s2, s3, s4 = st.columns(4)
s1.metric("Mean (Rata-rata Transaksi)", f"Rp {nilai.mean():,.0f}")
s2.metric("Median (Nilai Tengah)", f"Rp {nilai.median():,.0f}")
s3.metric("Std (Simpangan Baku)", f"Rp {nilai.std():,.0f}")
s4.metric("IQR (Q3 - Q1)", f"Rp {iqr:,.0f}")
st.divider()