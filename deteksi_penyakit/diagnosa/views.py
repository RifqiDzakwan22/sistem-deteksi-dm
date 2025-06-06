from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from .models import ManualPrediction

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

# ===== REGISTER & LOGIN USER =====
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'diagnosa/register.html', {'form': form})

def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('form_manual')
        else:
            return render(request, 'user_login.html', {'error': 'Username atau password salah'})
    return render(request, 'diagnosa/user_login.html')

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
        berat = float(request.POST.get('berat'))
        tinggi_cm = float(request.POST.get('tinggi'))
        tinggi_m = tinggi_cm / 100  # konversi ke meter
        bmi = round(berat / (tinggi_m ** 2), 2)  # rumus BMI
        riwayat = float(request.POST.get('riwayat'))
        usia = float(request.POST.get('usia'))

        input_data = np.array([[kehamilan, glukosa, tekanan, kulit, insulin, bmi, riwayat, usia]])
        pred_proba = model.predict_proba(input_data)[0][1]

        persen = round(pred_proba * 100, 2)
        risiko = round(persen * 0.7, 2)

        if persen < 40:
            tipe = "Normal atau Pra-Diabetes"
        elif jenis_kelamin.upper() == 'P' and kehamilan > 0 and glukosa > 140:
            tipe = "Kemungkinan Diabetes Gestasional"
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

        # Simpan ke database
        ManualPrediction.objects.create(
            user=request.user,
            jenis_kelamin=jenis_kelamin,
            kehamilan=kehamilan,
            glukosa=glukosa,
            tekanan=tekanan,
            kulit=kulit,
            insulin=insulin,
            berat=berat,
            tinggi=tinggi_cm,
            bmi=bmi,
            riwayat=riwayat,
            usia=usia,
            hasil_persen=persen,
            hasil_risiko=risiko,
            hasil_tipe=tipe,
            hasil_saran=saran
        )

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

# ===== REKAP ADMIN =====

# rekap data inputan manual
@user_passes_test(lambda u: u.is_superuser)
def rekap_admin(request):
    data = ManualPrediction.objects.all().order_by('-tanggal_input')
    return render(request, 'diagnosa/rekap_admin.html', {'data': data})

# rekap akun user
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def daftar_pengguna(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'diagnosa/daftar_pengguna.html', {'users': users})

# untuk menghapus akun user
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def hapus_pengguna(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
    except User.DoesNotExist:
        pass
    return redirect('daftar_pengguna')

# untuk menghapus data rekapan manual
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def hapus_prediksi_manual(request, prediksi_id):
    try:
        prediksi = ManualPrediction.objects.get(id=prediksi_id)
        prediksi.delete()
    except ManualPrediction.DoesNotExist:
        pass
    return redirect('rekap_admin')