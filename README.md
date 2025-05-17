# 🩺 Sistem Deteksi Dini Diabetes Menggunakan Decision Tree (Django)

Aplikasi ini merupakan sistem deteksi dini penyakit diabetes berbasis web yang dibangun dengan framework **Django** dan menggunakan algoritma **Decision Tree** sebagai model klasifikasi. Sistem ini memanfaatkan dataset *Pima Indians Diabetes* dan mengizinkan pengguna untuk menginput data kesehatan guna mendapatkan prediksi risiko diabetes secara cepat, akurat, dan mudah diakses.

---

## 🎯 Tujuan Proyek

- Membantu pengguna memeriksa kemungkinan mengidap diabetes secara mandiri.
- Menyediakan rekomendasi medis awal berdasarkan hasil prediksi.
- Menunjukkan penerapan algoritma Decision Tree dalam bidang kesehatan berbasis web.

---

## 🧪 Fitur Utama

- ✅ Form interaktif untuk input data pasien:
  - Jenis kelamin
  - Kehamilan (jika wanita)
  - Glukosa, Tekanan darah, Ketebalan kulit, Insulin
  - BMI, Riwayat diabetes keluarga, Usia
- 📊 Prediksi risiko diabetes dengan algoritma Decision Tree (entropy-based).
- 📈 Menampilkan persentase kemungkinan:
  - Mengidap diabetes
  - Risiko lanjut menjadi diabetes melitus
- 💡 Memberikan saran medis berdasarkan tingkat risiko
- 🌐 Dibangun dengan Django + scikit-learn + NumPy + Pandas

---

## ⚙️ Teknologi yang Digunakan

- Python 3.12+
- Django 5.2.1
- scikit-learn
- Pandas
- NumPy
- HTML5 & CSS3 (basic)

---

## 🚀 Cara Menjalankan Proyek

### 1. Clone Repository
```bash
git clone https://github.com/namamu/sistem-deteksi-diabetes.git
cd sistem-deteksi-diabetes
