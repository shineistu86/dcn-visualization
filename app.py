import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import re

st.set_page_config(
    page_title="DCN App Review Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

@st.cache_data
def load_data():
    df = pd.read_csv("data/dcn_crawlingdata_(1).csv")
    return df

df = load_data()

stopwords_core = set(STOPWORDS)
custom_stopwords = {
    'yg','yang','gak','ga','tidak','sdh','dgn','kalo','kalau',
    'bisa','ada','aja','udah','sudah','mau','lagi','bikin',
    'saya','aku','nya','ini','itu','dan','di','ke','dari',
    'buat','untuk','karena','juga','kok','sih','dong','kan',
    'banget','sangat','tolong','mohon','kasih','terima',
    'aplikasi','apk','dana','dompet','digital','uang','rupiah',
    'min','kak','bintang','kenapa','gimana','biar','padahal',
    'tapi','tetapi','atau','namun','masih','baru','kali'
}
final_stopwords = stopwords_core.union(custom_stopwords)

total_reviews = len(df)
avg_rating = df['score'].mean()

st.title("Dashboard Visualisasi Review Pengguna Aplikasi DANA")
st.markdown("---")

with st.expander("📄 Lihat Info Dataset"):
    st.subheader("Info Dataset")
    st.write(f"**Total Data:** {len(df):,} baris")

    st.subheader("Missing Value per Kolom")
    missing_df = pd.DataFrame({
        'Kolom': df.columns,
        'Missing Value': df.isnull().sum().values,
        'Persentase': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    st.dataframe(missing_df[missing_df['Missing Value'] > 0], hide_index=True, use_container_width=True)

    st.subheader("Tipe Data")
    dtype_df = pd.DataFrame({
        'Kolom': df.columns,
        'Tipe Data': df.dtypes.values
    })
    st.dataframe(dtype_df, hide_index=True, use_container_width=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Review", f"{total_reviews:,}")
with col2:
    st.metric("Rata-rata Rating", f"{avg_rating:.2f}")
with col3:
    st.metric("Total User", f"{df['userName'].nunique():,}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Rating Distribution", "Tren Review Harian", "Text Mining"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(x='score', data=df, palette='viridis', ax=ax)
        ax.set_xlabel('Rating')
        ax.set_ylabel('Jumlah')
        ax.set_title('')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True)

    with col2:
        rating_counts = df['score'].value_counts().sort_index()
        rating_percent = rating_counts / rating_counts.sum() * 100
        colors = plt.cm.Set2(range(len(rating_percent)))
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(rating_percent, labels=rating_percent.index,
                autopct='%1.1f%%', startangle=90, colors=colors, explode=[0.02]*len(rating_percent))
        ax.axis('equal')
        st.pyplot(fig, use_container_width=True)

with tab2:
    df['review_datetime'] = pd.to_datetime(df['review_datetime'], errors='coerce')
    daily_trend = df['review_datetime'].dropna().dt.date.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(daily_trend.index, daily_trend.values, marker='o', linewidth=2, markersize=4, color='#2ecc71')
    ax.fill_between(daily_trend.index, daily_trend.values, alpha=0.3, color='#2ecc71')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Review')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with tab3:
    clean_corpus = df['content'].dropna().apply(lambda x: str(x).lower())
    all_text_string = " ".join(clean_corpus)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Wordcloud Global")
        wordcloud = WordCloud(width=400, height=300, background_color='white',
                              stopwords=final_stopwords, max_words=80, colormap='viridis').generate(all_text_string)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with col2:
        st.subheader("Wordcloud per Rating")
        selected_rating = st.selectbox("Pilih Rating", [1, 2, 3, 4, 5], key="rating_select")
        subset_text = " ".join(df[df['score'] == selected_rating]['content'].dropna().astype(str))
        subset_text = re.sub(r'[^\w\s]', '', subset_text).lower()
        wc = WordCloud(width=400, height=300, background_color='white',
                       stopwords=final_stopwords, max_words=80, colormap='magma').generate(subset_text)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Top 50 Kata Kunci")
    words = all_text_string.split()
    filtered_words = [w for w in words if w not in final_stopwords and len(w) > 2]
    word_freq = Counter(filtered_words).most_common(50)
    df_words = pd.DataFrame(word_freq, columns=['Kata', 'Frekuensi'])

    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(data=df_words, x='Frekuensi', y='Kata', palette='viridis', ax=ax)
    ax.set_xlabel('Frekuensi')
    ax.set_ylabel('')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

st.markdown("---")
st.markdown("<center>© 2026 DCN App Review Analysis Dashboard</center>", unsafe_allow_html=True)
