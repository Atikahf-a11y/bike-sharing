import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")

SEASON_ORDER = ["Spring", "Summer", "Fall", "Winter"]
SEASON_COLORS = {
    "Spring": "#A8DADC",
    "Summer": "#457B9D",
    "Fall": "#F4A261",
    "Winter": "#8D99AE",
}
DAY_ORDER = ["Working Day", "Weekend/Holiday"]
DEMAND_ORDER = ["Rendah", "Sedang", "Tinggi"]

st.set_page_config(
    page_title="Dashboard Bike Sharing",
    page_icon="🚲",
    layout="wide",
)


@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_data.csv")
    df = pd.read_csv(path, parse_dates=["dteday"])
    return df


def fmt(angka):
    """Format angka ribuan dengan titik (gaya Indonesia)."""
    return f"{angka:,.0f}".replace(",", ".")


def fmt_persen(angka):
    return f"{angka:.2f}".replace(".", ",") + "%"


day_df = load_data()

# ---------------------------------------------------------------- Sidebar
with st.sidebar:
    st.title("🚲 Filter Data")

    min_date = day_df["dteday"].min().date()
    max_date = day_df["dteday"].max().date()
    rentang = st.date_input(
        "Rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    pilih_musim = st.multiselect(
        "Musim", options=SEASON_ORDER, default=SEASON_ORDER
    )
    pilih_hari = st.multiselect(
        "Jenis hari", options=DAY_ORDER, default=DAY_ORDER
    )

    st.caption(
        "Sumber data: Bike Sharing Dataset (Capital Bikeshare, "
        "Washington D.C., 2011–2012)."
    )

# Rentang tanggal bisa berisi 1 tanggal saja saat pengguna masih memilih
if isinstance(rentang, (tuple, list)) and len(rentang) == 2:
    tgl_awal, tgl_akhir = rentang
else:
    tgl_awal, tgl_akhir = min_date, max_date

filtered = day_df[
    (day_df["dteday"].dt.date >= tgl_awal)
    & (day_df["dteday"].dt.date <= tgl_akhir)
    & (day_df["season_label"].isin(pilih_musim))
    & (day_df["day_type"].isin(pilih_hari))
]

# ---------------------------------------------------------------- Header
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown(
    "Analisis pola penyewaan sepeda Capital Bikeshare (Washington D.C.) "
    "periode 2011–2012 berdasarkan **musim** dan **segmen pengguna**."
)

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih. Ubah filter di sidebar.")
    st.stop()

# ---------------------------------------------------------------- KPI
total_cnt = filtered["cnt"].sum()
total_casual = filtered["casual"].sum()
total_registered = filtered["registered"].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Penyewaan", fmt(total_cnt))
k2.metric("Rata-rata per Hari", fmt(filtered["cnt"].mean()))
k3.metric("Pengguna Registered", fmt_persen(total_registered / total_cnt * 100))
k4.metric("Pengguna Casual", fmt_persen(total_casual / total_cnt * 100))

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Pertanyaan 1: Musim",
        "Pertanyaan 2: Casual vs Registered",
        "Analisis Lanjutan",
        "Kesimpulan & Rekomendasi",
    ]
)

# ---------------------------------------------------------------- Pertanyaan 1
with tab1:
    st.subheader("Perbedaan rata-rata penyewaan sepeda antar musim")
    st.caption(
        "Pertanyaan 1: Bagaimana perbedaan rata-rata penyewaan sepeda antara "
        "musim Spring, Summer, Fall, dan Winter selama periode 2011–2012?"
    )

    season_analysis = (
        filtered.groupby("season_label")
        .agg(
            jumlah_hari=("cnt", "count"),
            total_penyewaan=("cnt", "sum"),
            rata_rata_penyewaan=("cnt", "mean"),
            median_penyewaan=("cnt", "median"),
        )
        .reindex([s for s in SEASON_ORDER if s in filtered["season_label"].unique()])
        .round(2)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=season_analysis.reset_index(),
        x="season_label",
        y="rata_rata_penyewaan",
        hue="season_label",
        order=season_analysis.index.tolist(),
        palette=SEASON_COLORS,
        legend=False,
        ax=ax,
    )
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)
    ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Musim",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-Rata Penyewaan per Hari")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Tren rata-rata per bulan
    nama_bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
                  "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    monthly = filtered.groupby("mnth")["cnt"].mean().reindex(range(1, 13))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly.index, monthly.values, marker="o", markersize=8,
            linewidth=2.5, color="#219EBC")
    for bulan, nilai in monthly.items():
        ax.annotate(f"{nilai:,.0f}", (bulan, nilai), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontsize=9)
    ax.set_title("Tren Rata-Rata Penyewaan Sepeda Berdasarkan Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-Rata Penyewaan per Hari")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(nama_bulan)
    ax.grid(axis="y", alpha=0.3)
    sns.despine()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    tertinggi = season_analysis["rata_rata_penyewaan"].idxmax()
    terendah = season_analysis["rata_rata_penyewaan"].idxmin()
    st.info(
        f"**Insight:** pada data yang difilter, musim **{tertinggi}** memiliki rata-rata "
        f"penyewaan tertinggi ({fmt(season_analysis.loc[tertinggi, 'rata_rata_penyewaan'])} per hari), "
        f"sedangkan musim **{terendah}** terendah "
        f"({fmt(season_analysis.loc[terendah, 'rata_rata_penyewaan'])} per hari)."
    )

    with st.expander("Lihat tabel ringkasan per musim"):
        st.dataframe(season_analysis)

# ---------------------------------------------------------------- Pertanyaan 2
with tab2:
    st.subheader("Komposisi pengguna Casual dan Registered berdasarkan jenis hari")
    st.caption(
        "Pertanyaan 2: Bagaimana perbandingan persentase penyewaan pengguna casual dan "
        "registered terhadap total penyewaan pada hari kerja dan hari non-kerja "
        "(akhir pekan dan hari libur) selama periode 2011–2012?"
    )

    user_analysis = (
        filtered.groupby("day_type")
        .agg(
            total_casual=("casual", "sum"),
            total_registered=("registered", "sum"),
            total_penyewaan=("cnt", "sum"),
            rata_rata_casual=("casual", "mean"),
            rata_rata_registered=("registered", "mean"),
        )
        .reindex([d for d in DAY_ORDER if d in filtered["day_type"].unique()])
    )
    user_analysis["persentase_casual"] = (
        user_analysis["total_casual"] / user_analysis["total_penyewaan"] * 100
    )
    user_analysis["persentase_registered"] = (
        user_analysis["total_registered"] / user_analysis["total_penyewaan"] * 100
    )

    plot_user = user_analysis[["persentase_casual", "persentase_registered"]]
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_user.plot(
        kind="bar",
        stacked=True,
        color=["#F4A261", "#457B9D"],
        width=0.55,
        ax=ax,
    )
    for container in ax.containers:
        labels = [
            f"{bar.get_height():.1f}%" if bar.get_height() > 0 else ""
            for bar in container
        ]
        ax.bar_label(
            container,
            labels=labels,
            label_type="center",
            color="white",
            fontweight="bold",
        )
    ax.set_title(
        "Komposisi Pengguna Casual dan Registered Berdasarkan Jenis Hari",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Jenis Hari")
    ax.set_ylabel("Persentase Penyewaan (%)")
    ax.set_ylim(0, 100)
    ax.legend(
        ["Casual", "Registered"],
        title="Segmen Pengguna",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
    )
    plt.setp(ax.get_xticklabels(), rotation=0)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.boxplot(
        data=filtered,
        x="season_label",
        y="cnt",
        order=[s for s in SEASON_ORDER if s in filtered["season_label"].unique()],
        hue="season_label",
        palette=SEASON_COLORS,
        legend=False,
        width=0.55,
        ax=ax,
    )
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan Sepeda per Hari")
    sns.despine()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    ringkas = []
    for jenis, baris in user_analysis.iterrows():
        ringkas.append(
            f"pada **{jenis}**, Registered berkontribusi "
            f"{fmt_persen(baris['persentase_registered'])} dan Casual "
            f"{fmt_persen(baris['persentase_casual'])}"
        )
    st.info("**Insight:** " + "; ".join(ringkas) + ".")

    with st.expander("Lihat tabel ringkasan per jenis hari"):
        st.dataframe(user_analysis.round(2))

# ---------------------------------------------------------------- Analisis lanjutan
with tab3:
    st.subheader("Distribusi tingkat permintaan berdasarkan musim")
    st.caption(
        "Jumlah penyewaan harian dikelompokkan dengan teknik binning (kuantil) menjadi "
        "kategori Rendah, Sedang, dan Tinggi."
    )

    demand_season = (
        pd.crosstab(filtered["season_label"], filtered["kategori_permintaan"], normalize="index")
        .mul(100)
        .reindex(index=[s for s in SEASON_ORDER if s in filtered["season_label"].unique()],
                 columns=DEMAND_ORDER, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    demand_season.plot(kind="bar", stacked=True,
                       color=["#E9C46A", "#2A9D8F", "#457B9D"], ax=ax)
    ax.set_title("Distribusi Tingkat Permintaan Berdasarkan Musim", fontweight="bold")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Persentase Hari (%)")
    ax.legend(title="Tingkat Permintaan", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.setp(ax.get_xticklabels(), rotation=0)
    sns.despine()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Lihat tabel persentase"):
        st.dataframe(demand_season.round(2))

# ---------------------------------------------------------------- Kesimpulan
with tab4:
    st.subheader("Kesimpulan")
    st.markdown(
        """
**Pertanyaan 1 (musim).** Pada seluruh data 2011–2012, musim **Fall** memiliki rata-rata
penyewaan tertinggi (±5.644 per hari), diikuti Summer (±4.992) dan Winter (±4.728),
sedangkan musim **Spring** terendah (±2.604 per hari). Musim berkaitan erat dengan
variasi permintaan penyewaan sepeda.

**Pertanyaan 2 (segmen pengguna).** Pengguna **Registered** mendominasi penyewaan pada
hari kerja (±86,77%), sedangkan kontribusi pengguna **Casual** naik menjadi ±31,66%
pada hari non-kerja (akhir pekan dan hari libur).
"""
    )

    st.subheader("Rekomendasi Action Item")
    st.markdown(
        """
1. **Atur armada berdasarkan musim.** Tambah ketersediaan dan perawatan sepeda menjelang
   musim Fall dan Summer yang permintaannya tinggi, serta manfaatkan musim Spring yang
   permintaannya rendah untuk perawatan armada atau program promosi.
2. **Pengguna Registered (hari kerja).** Fokuskan pada program loyalitas, penawaran
   perpanjangan keanggotaan, dan paket langganan untuk perjalanan rutin.
3. **Pengguna Casual (akhir pekan/libur).** Arahkan pada promosi akhir pekan, paket
   penyewaan harian, dan kampanye rekreasi untuk mendorong pengguna non-berlangganan.
"""
    )

st.caption("Proyek Analisis Data · Dicoding · Bike Sharing Dataset")
