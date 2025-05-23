from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# ====== TRAINING SEKALI DI AWAL ======
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ['Kehamilan', 'Glukosa', 'TekananDarah', 'KetebalanKulit',
           'Insulin', 'BMI', 'RiwayatDiabetesKeluarga', 'Usia', 'Hasil']
data = pd.read_csv(url, names=columns)

X = data.drop('Hasil', axis=1)
y = data['Hasil']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ====== VIEW FORM ======
@login_required(login_url='login')
def form_prediksi(request):
    return render(request, "diagnosa/form.html")

# ====== VIEW HASIL ======
@login_required(login_url='login')
def hasil_prediksi(request):
    if request.method == "POST":
        jenis_kelamin = request.POST.get("jenis_kelamin")
        kehamilan = float(request.POST.get("kehamilan")) if jenis_kelamin.upper() == "P" else 0
        glukosa = float(request.POST.get("glukosa"))
        tekanan = float(request.POST.get("tekanan"))
        kulit = float(request.POST.get("kulit"))
        insulin = float(request.POST.get("insulin"))
        bmi = float(request.POST.get("bmi"))
        riwayat = float(request.POST.get("riwayat"))
        usia = float(request.POST.get("usia"))

        input_data = np.array([[kehamilan, glukosa, tekanan, kulit, insulin, bmi, riwayat, usia]])
        prediksi_proba = model.predict_proba(input_data)[0]
        prediksi = model.predict(input_data)

        persen = round(prediksi_proba[1] * 100, 2)
        risiko = round(persen * 0.7, 2)

        if persen < 40:
            tipe = "Normal atau Pra-Diabetes"
        elif usia <= 25 and insulin < 50 and bmi < 22:
            tipe = "Kemungkinan Diabetes Tipe 1"
        elif usia >= 30 and bmi > 25:
            tipe = "Kemungkinan Diabetes Tipe 2"
        else:
            tipe = "Perlu pemeriksaan lebih lanjut untuk memastikan tipe"

        if persen >= 70:
            saran = "⚠️ Segera konsultasikan ke dokter spesialis penyakit dalam dan lakukan tes lanjutan seperti HbA1c dan gula darah puasa."
        elif persen >= 40:
            saran = "⚠️ Risiko sedang. Disarankan mulai menjaga pola makan, olahraga rutin, dan periksa gula darah berkala."
        else:
            saran = "✅ Risiko rendah. Tetap pertahankan gaya hidup sehat dan lakukan skrining setiap 6 bulan."

        context = {
            "persen": persen,
            "risiko": risiko,
            "saran": saran,
            "tipe": tipe,
            "prediksi": prediksi,
        }
        return render(request, "diagnosa/hasil.html", context)
    else:
        return redirect('form_prediksi')
