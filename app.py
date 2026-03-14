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
    initial_sidebar_state="expanded"
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
    .icon-header {
        display: inline-flex;
        align-items: center;
        gap: 10px;
    }
    .bi {
        font-size: 1.5em;
        vertical-align: middle;
    }
    .sentiment-positive { color: #27ae60; font-weight: bold; }
    .sentiment-neutral { color: #f39c12; font-weight: bold; }
    .sentiment-negative { color: #e74c3c; font-weight: bold; }
</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.min.css">
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

def get_sentiment(score):
    if score >= 4:
        return 'Positive'
    elif score == 3:
        return 'Neutral'
    else:
        return 'Negative'

df['sentiment'] = df['score'].apply(get_sentiment)

st.markdown('<div class="icon-header"><i class="bi bi-bar-chart-fill"></i><h1>DCN App Review Analysis</h1></div>', unsafe_allow_html=True)
st.markdown("Dashboard interaktif untuk menganalisis review pengguna aplikasi dompet digital")
st.markdown("---")

with st.sidebar:
    st.markdown('<div class="icon-header"><i class="bi bi-funnel"></i><h3>Filter</h3></div>', unsafe_allow_html=True)
    
    selected_ratings = st.multiselect(
        "Filter Rating",
        options=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5]
    )
    
    selected_sentiments = st.multiselect(
        "Filter Sentimen",
        options=['Positive', 'Neutral', 'Negative'],
        default=['Positive', 'Neutral', 'Negative']
    )
    
    df_filtered = df[
        df['score'].isin(selected_ratings) & 
        df['sentiment'].isin(selected_sentiments)
    ]
    
    st.markdown("---")
    st.markdown('<div class="icon-header"><i class="bi bi-clipboard-data"></i><h3>Info Data</h3></div>', unsafe_allow_html=True)
    st.metric("Total Review", f"{len(df_filtered):,}")
    
    st.markdown("---")
    st.markdown('<i class="bi bi-exclamation-triangle"></i> Missing Value', unsafe_allow_html=True)
    missing_df = pd.DataFrame({
        'Kolom': df_filtered.columns,
        'Missing': df_filtered.isnull().sum().values
    })
    st.dataframe(missing_df[missing_df['Missing'] > 0], hide_index=True, use_container_width=True)

if len(df_filtered) == 0:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

positive_count = len(df_filtered[df_filtered['sentiment'] == 'Positive'])
neutral_count = len(df_filtered[df_filtered['sentiment'] == 'Neutral'])
negative_count = len(df_filtered[df_filtered['sentiment'] == 'Negative'])
total_reviews = len(df_filtered)
avg_rating = df_filtered['score'].mean()
positive_pct = (positive_count / total_reviews) * 100 if total_reviews > 0 else 0

st.markdown('<div class="icon-header"><i class="bi bi-speedometer2"></i><h3>Overview</h3></div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Review", f"{total_reviews:,}")
with col2:
    st.metric("Rata-rata Rating", f"{avg_rating:.2f}")
with col3:
    st.metric("Positive Review", f"{positive_pct:.1f}%")
with col4:
    st.metric("Total User", f"{df_filtered['userName'].nunique():,}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Overview", "Review Analysis", "Text Mining"])

with tab1:
    st.markdown("### Rating Distribution")
    col1, col2 = st.columns(2)

    with col1:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.countplot(x='score', data=df_filtered, palette='viridis', ax=ax3)
        ax3.set_xlabel('Rating')
        ax3.set_ylabel('Jumlah')
        ax3.set_title('')
        ax3.grid(axis='y', alpha=0.3)
        st.pyplot(fig3, use_container_width=True)

    with col2:
        rating_counts = df_filtered['score'].value_counts().sort_index()
        rating_percent = rating_counts / rating_counts.sum() * 100
        colors = plt.cm.Set2(range(len(rating_percent)))
        fig1, ax1 = plt.subplots(figsize=(5, 5))
        ax1.pie(rating_percent, labels=rating_percent.index,
                autopct='%1.1f%%', startangle=90, colors=colors, explode=[0.02]*len(rating_percent))
        ax1.axis('equal')
        st.pyplot(fig1, use_container_width=True)

with tab2:
    st.markdown("### Tren Review Harian")
    df_filtered = df_filtered.copy()
    df_filtered['review_datetime'] = pd.to_datetime(df_filtered['review_datetime'], errors='coerce')
    daily_trend = df_filtered['review_datetime'].dropna().dt.date.value_counts().sort_index()
    
    fig5, ax5 = plt.subplots(figsize=(10, 3))
    ax5.plot(daily_trend.index, daily_trend.values, marker='o', linewidth=2, markersize=4, color='#2ecc71')
    ax5.fill_between(daily_trend.index, daily_trend.values, alpha=0.3, color='#2ecc71')
    ax5.set_xlabel('Tanggal')
    ax5.set_ylabel('Jumlah Review')
    ax5.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig5, use_container_width=True)
    
with tab3:
    st.markdown("### Wordcloud Global")
    clean_corpus = df_filtered['content'].dropna().apply(lambda x: str(x).lower())
    all_text_string = " ".join(clean_corpus)
    
    wordcloud = WordCloud(width=400, height=300, background_color='white',
                          stopwords=final_stopwords, max_words=80, colormap='viridis').generate(all_text_string)
    
    col1, col2 = st.columns(2)
    with col1:
        fig8, ax8 = plt.subplots(figsize=(5, 4))
        ax8.imshow(wordcloud, interpolation='bilinear')
        ax8.axis('off')
        plt.tight_layout()
        st.pyplot(fig8, use_container_width=True)
    
    with col2:
        st.markdown("#### Wordcloud per Rating")
        selected_rating = st.selectbox("Pilih Rating", [1, 2, 3, 4, 5], key="rating_select")
        subset_text = " ".join(df_filtered[df_filtered['score'] == selected_rating]['content'].dropna().astype(str))
        subset_text = re.sub(r'[^\w\s]', '', subset_text).lower()
        wc = WordCloud(width=400, height=300, background_color='white',
                       stopwords=final_stopwords, max_words=80, colormap='magma').generate(subset_text)
        fig9, ax9 = plt.subplots(figsize=(5, 4))
        ax9.imshow(wc, interpolation='bilinear')
        ax9.axis('off')
        plt.tight_layout()
        st.pyplot(fig9, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Top 50 Kata Kunci")
    words = all_text_string.split()
    filtered_words = [w for w in words if w not in final_stopwords and len(w) > 2]
    word_freq = Counter(filtered_words).most_common(50)
    df_words = pd.DataFrame(word_freq, columns=['Kata', 'Frekuensi'])
    
    fig10, ax10 = plt.subplots(figsize=(8, 10))
    sns.barplot(data=df_words, x='Frekuensi', y='Kata', palette='viridis', ax=ax10)
    ax10.set_xlabel('Frekuensi')
    ax10.set_ylabel('')
    ax10.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig10, use_container_width=True)

st.markdown("---")
st.markdown("<center>© 2026 DCN App Review Analysis Dashboard</center>", unsafe_allow_html=True)
