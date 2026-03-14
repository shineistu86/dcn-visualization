# Import library yang dibutuhkan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import re

# Konfigurasi halaman streamlit
st.set_page_config(
    page_title="DCN App Review Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS custom untuk styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stDataFrame {
        border-radius: 10px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk load data
def loadData():
    df = pd.read_csv("data/dcn_crawlingdata_(1).csv")
    return df

# Load data ke variabel dataframe
dataframe = loadData()

# Daftar stopwords untuk text mining
stopwords_inti = set(STOPWORDS)
stopwords_tambahan = {
    'yg','yang','gak','ga','tidak','sdh','dgn','kalo','kalau',
    'bisa','ada','aja','udah','sudah','mau','lagi','bikin',
    'saya','aku','nya','ini','itu','dan','di','ke','dari',
    'buat','untuk','karena','juga','kok','sih','dong','kan',
    'banget','sangat','tolong','mohon','kasih','terima',
    'aplikasi','apk','dana','dompet','digital','uang','rupiah',
    'min','kak','bintang','kenapa','gimana','biar','padahal',
    'tapi','tetapi','atau','namun','masih','baru','kali'
}
# Gabungkan stopwords
stopwords_akhir = stopwords_inti.union(stopwords_tambahan)

# Hitung total review dan rata-rata rating
jumlah_review = len(dataframe)
rata_rata_rating = dataframe['score'].mean()

# Judul dashboard
st.title("Dashboard Visualisasi Review Pengguna Aplikasi DANA")
st.markdown("---")

# Menampilkan info dataset
with st.expander("Lihat Info Dataset"):
    st.subheader("Info Dataset")
    st.write(f"**Total Data:** {len(dataframe):,} baris")

    st.subheader("Missing Value per Kolom")
    df_missing = pd.DataFrame({
        'Kolom': dataframe.columns,
        'Missing Value': dataframe.isnull().sum().values,
        'Persentase': (dataframe.isnull().sum().values / len(dataframe) * 100).round(2)
    })
    st.dataframe(df_missing[df_missing['Missing Value'] > 0], hide_index=True, use_container_width=True)

    st.subheader("Tipe Data")
    df_tipe = pd.DataFrame({
        'Kolom': dataframe.columns,
        'Tipe Data': dataframe.dtypes.values
    })
    st.dataframe(df_tipe, hide_index=True, use_container_width=True)

st.markdown("---")

# Menampilkan metric utama
kolom1, kolom2, kolom3 = st.columns(3)
with kolom1:
    st.metric("Total Review", f"{jumlah_review:,}")
with kolom2:
    st.metric("Rata-rata Rating", f"{rata_rata_rating:.2f}")
with kolom3:
    st.metric("Total User", f"{dataframe['userName'].nunique():,}")

st.markdown("---")

# Membuat tabs untuk visualisasi
tab1, tab2, tab3 = st.tabs(["Rating Distribution", "Tren Review Harian", "Text Mining"])

# Tab 1: Rating Distribution
with tab1:
    k1, k2 = st.columns(2)

    with k1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(x='score', data=dataframe, palette='viridis', ax=ax)
        ax.set_xlabel('Rating')
        ax.set_ylabel('Jumlah')
        ax.set_title('')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True)

    with k2:
        hitung_rating = dataframe['score'].value_counts().sort_index()
        persen_rating = hitung_rating / hitung_rating.sum() * 100
        warna = plt.cm.Set2(range(len(persen_rating)))
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(persen_rating, labels=persen_rating.index,
                autopct='%1.1f%%', startangle=90, colors=warna, explode=[0.02]*len(persen_rating))
        ax.axis('equal')
        st.pyplot(fig, use_container_width=True)

# Tab 2: Tren Review Harian
with tab2:
    dataframe['review_datetime'] = pd.to_datetime(dataframe['review_datetime'], errors='coerce')
    tren_harian = dataframe['review_datetime'].dropna().dt.date.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(tren_harian.index, tren_harian.values, marker='o', linewidth=2, markersize=4, color='#2ecc71')
    ax.fill_between(tren_harian.index, tren_harian.values, alpha=0.3, color='#2ecc71')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Review')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Tab 3: Text Mining
with tab3:
    # Bersihkan text untuk wordcloud
    text_bersih = dataframe['content'].dropna().apply(lambda x: str(x).lower())
    semua_text = " ".join(text_bersih)

    k1, k2 = st.columns(2)

    with k1:
        st.subheader("Wordcloud Global")
        wordcloud = WordCloud(width=400, height=300, background_color='white',
                              stopwords=stopwords_akhir, max_words=80, colormap='viridis').generate(semua_text)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with k2:
        st.subheader("Wordcloud per Rating")
        pilih_rating = st.selectbox("Pilih Rating", [1, 2, 3, 4, 5], key="rating_select")
        text_per_rating = " ".join(dataframe[dataframe['score'] == pilih_rating]['content'].dropna().astype(str))
        text_per_rating = re.sub(r'[^\w\s]', '', text_per_rating).lower()
        wc = WordCloud(width=400, height=300, background_color='white',
                       stopwords=stopwords_akhir, max_words=80, colormap='magma').generate(text_per_rating)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Top 100 Kata Kunci")
    # Hitung frekuensi kata
    kata_kata = semua_text.split()
    kata_filter = [w for w in kata_kata if w not in stopwords_akhir and len(w) > 2]
    freq_kata = Counter(kata_filter).most_common(100)
    df_kata = pd.DataFrame(freq_kata, columns=['Kata', 'Frekuensi'])

    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(data=df_kata, x='Frekuensi', y='Kata', palette='viridis', ax=ax)
    ax.set_xlabel('Frekuensi')
    ax.set_ylabel('')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
