# DCN App Review Visualization

Dashboard interaktif untuk menganalisis review pengguna aplikasi dompet digital menggunakan Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

- **Interactive Filtering** - Filter by rating dan sentimen
- **Sentiment Analysis** - Klasifikasi otomatis (Positive/Neutral/Negative)
- **Rating Distribution** - Visualisasi distribusi rating pengguna
- **Daily Review Trends** - Analisis tren review harian
- **Wordcloud Visualization** - Visualisasi kata kunci dominan
- **Keyword Frequency Analysis** - Top 50 kata kunci paling sering muncul
- **Review Length Analysis** - Analisis panjang review vs rating
- **Professional UI** - Tampilan bersih dengan Bootstrap Icons

## 🛠️ Tech Stack

- **Python** - Bahasa pemrograman utama
- **Streamlit** - Framework untuk web app interaktif
- **Pandas** - Manipulasi dan analisis data
- **Matplotlib** - Visualisasi data
- **Seaborn** - Statistical data visualization
- **WordCloud** - Visualisasi word cloud

## 📊 Dashboard Preview

![Dashboard Preview](assets/preview_dashboard.png)

## 📁 Dataset

Dataset berisi hasil crawling review aplikasi dengan atribut:

| Kolom | Deskripsi |
|-------|-----------|
| `reviewId` | ID unik review |
| `userName` | Nama pengguna |
| `content` | Isi review text |
| `score` | Rating (1-5) |
| `review_datetime` | Tanggal dan waktu review |
| `thumbsUpCount` | Jumlah thumbs up |
| `replyContent` | Balasan dari developer |

## 🚀 Quick Start

### Clone Repository

```bash
git clone https://github.com/shineistu86/dcn-visualization.git
cd dcn-visualization
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Streamlit

```bash
streamlit run app.py
```

Dashboard akan terbuka di browser Anda pada `http://localhost:8501`

## 📂 Project Structure

```
dcn-visualization/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── data/
│   └── dcn_crawlingdata_(1).csv    # Dataset
└── assets/
    └── preview_dashboard.png   # Dashboard screenshot
```

## 📈 Sentiment Classification

| Sentimen | Rating | Warna |
|----------|--------|-------|
| Positive | 4-5    | 🟢 Hijau |
| Neutral  | 3      | 🟠 Kuning |
| Negative | 1-2    | 🔴 Merah |

## 🎯 Usage

1. **Overview Tab** - Lihat ringkasan metrik dan distribusi sentimen
2. **Review Analysis Tab** - Analisis tren harian dan review length
3. **Text Mining Tab** - Eksplorasi wordcloud dan keyword frequency
4. **Sidebar Filter** - Filter data berdasarkan rating dan sentimen

## 🌐 Live Demo

Streamlit Cloud:

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dcn-visualization.streamlit.app)

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**shineistu86**

GitHub: [@shineistu86](https://github.com/shineistu86)

## 🙏 Acknowledgments

- Dataset dari Google Play Store reviews
- Built with ❤️ using Streamlit

---

<p align="center">© 2026 DCN App Review Analysis Dashboard</p>
