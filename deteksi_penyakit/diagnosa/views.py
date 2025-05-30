from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Latih model sekali saat server dijalankan
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ['Kehamilan', 'Glukosa', 'TekananDarah', 'KetebalanKulit',
           'Insulin', 'BMI', 'RiwayatDiabetesKeluarga', 'Usia', 'Hasil']
data = pd.read_csv(url, names=columns)

X = data.drop('Hasil', axis=1)
y = data['Hasil']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ===== VIEW UNTUK HOME =====
@login_required(login_url='login')
def home(request):
    return render(request, 'diagnosa/home.html')

# ===== LOGOUT =====
def logout_user(request):
    logout(request)
    return redirect('login')

# ===== INPUT MANUAL =====
@login_required(login_url='login')
def form_manual(request):
    return render(request, 'diagnosa/form_manual.html')

@login_required(login_url='login')
def hasil_prediksi(request):
    if request.method == 'POST':
        jenis_kelamin = request.POST.get('jenis_kelamin')
        kehamilan = float(request.POST.get('kehamilan')) if jenis_kelamin.upper() == 'P' else 0
        glukosa = float(request.POST.get('glukosa'))
        tekanan = float(request.POST.get('tekanan'))
        kulit = float(request.POST.get('kulit'))
        insulin = float(request.POST.get('insulin'))
        bmi = float(request.POST.get('bmi'))
        riwayat = float(request.POST.get('riwayat'))
        usia = float(request.POST.get('usia'))

        input_data = np.array([[kehamilan, glukosa, tekanan, kulit, insulin, bmi, riwayat, usia]])
        pred_proba = model.predict_proba(input_data)[0][1]

        persen = round(pred_proba * 100, 2)
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
            saran = "⚠️ Segera konsultasi ke dokter spesialis penyakit dalam."
        elif persen >= 40:
            saran = "⚠️ Risiko sedang. Jaga pola makan dan olahraga."
        else:
            saran = "✅ Risiko rendah. Tetap gaya hidup sehat."

        context = {
            'persen': persen,
            'risiko': risiko,
            'tipe': tipe,
            'saran': saran,
        }
        return render(request, 'diagnosa/hasil_manual.html', context)
    else:
        return redirect('form_manual')

# ===== UPLOAD CSV =====
@login_required(login_url='login')
def form_upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('csv_file')
        if not uploaded_file:
            return render(request, 'diagnosa/form_upload.html', {'error': 'File tidak ditemukan'})

        try:
            df = pd.read_csv(uploaded_file)

            # Pastikan kolom 'Hasil' ada
            if 'Hasil' not in df.columns:
                return render(request, 'diagnosa/form_upload.html', {'error': "'Hasil' tidak ditemukan dalam file"})

            if df.shape[0] < 100:
                return render(request, 'diagnosa/form_upload.html', {'error': 'Minimal 100 baris data diperlukan'})

            X = df.drop('Hasil', axis=1)
            y_true = df['Hasil']
            y_pred = model.predict(X)

            report = classification_report(y_true, y_pred, output_dict=True)
            accuracy = round(accuracy_score(y_true, y_pred) * 100, 2)

            context = {
                'accuracy': accuracy,
                'macro_precision': round(report['macro avg']['precision'], 2),
                'macro_recall': round(report['macro avg']['recall'], 2),
                'macro_f1': round(report['macro avg']['f1-score'], 2),
                'support': int(report['macro avg']['support'])
            }
            return render(request, 'diagnosa/hasil_upload.html', context)

        except Exception as e:
            return render(request, 'diagnosa/form_upload.html', {'error': f'Terjadi kesalahan: {str(e)}'})

    return render(request, 'diagnosa/form_upload.html')
