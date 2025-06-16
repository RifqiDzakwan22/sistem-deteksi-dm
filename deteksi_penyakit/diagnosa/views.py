from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import ManualPrediction
from django.contrib.auth.forms import AuthenticationForm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# ===== Model Training Once =====
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ['Kehamilan', 'Glukosa', 'TekananDarah', 'KetebalanKulit',
           'Insulin', 'BMI', 'RiwayatDiabetesKeluarga', 'Usia', 'Hasil']
data = pd.read_csv(url, names=columns)

X = data.drop('Hasil', axis=1)
y = data['Hasil']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ===== Views =====
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'diagnosa/home.html'
    login_url = 'login'


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'diagnosa/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        return render(request, 'diagnosa/register.html', {'form': form})


class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'diagnosa/login.html', {'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'diagnosa/login.html', {'error': 'Username atau password salah'})


class FormManualView(LoginRequiredMixin, TemplateView):
    template_name = 'diagnosa/form_manual.html'
    login_url = 'login'


class HasilPrediksiView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request):
        jenis_kelamin = request.POST.get('jenis_kelamin')
        kehamilan = float(request.POST.get('kehamilan')) if jenis_kelamin.upper() == 'P' else 0
        glukosa = float(request.POST.get('glukosa'))
        tekanan = float(request.POST.get('tekanan'))
        kulit = float(request.POST.get('kulit'))
        insulin = float(request.POST.get('insulin'))
        berat = float(request.POST.get('berat'))
        tinggi_cm = float(request.POST.get('tinggi'))
        tinggi_m = tinggi_cm / 100
        bmi = round(berat / (tinggi_m ** 2), 2)
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

        saran = (
            "⚠️ Segera konsultasi ke dokter spesialis penyakit dalam."
            if persen >= 70 else
            "⚠️ Risiko sedang. Jaga pola makan dan olahraga."
            if persen >= 40 else
            "✅ Risiko rendah. Tetap gaya hidup sehat."
        )

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

        return render(request, 'diagnosa/hasil_manual.html', {
            'persen': persen,
            'risiko': risiko,
            'tipe': tipe,
            'saran': saran
        })

    def get(self, request):
        return redirect('form_manual')


class UploadCSVView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'diagnosa/form_upload.html')

    def post(self, request):
        uploaded_file = request.FILES.get('csv_file')
        if not uploaded_file:
            return render(request, 'diagnosa/form_upload.html', {'error': 'File tidak ditemukan'})

        try:
            df = pd.read_csv(uploaded_file)

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


class RekapAdminView(UserPassesTestMixin, ListView):
    model = ManualPrediction
    template_name = 'diagnosa/rekap_admin.html'
    context_object_name = 'data'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return ManualPrediction.objects.all().order_by('-tanggal_input')


class DaftarPenggunaView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'diagnosa/daftar_pengguna.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class HapusPenggunaView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
        except User.DoesNotExist:
            pass
        return redirect('daftar_pengguna')


class HapusPrediksiManualView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, prediksi_id):
        try:
            prediksi = ManualPrediction.objects.get(id=prediksi_id)
            prediksi.delete()
        except ManualPrediction.DoesNotExist:
            pass
        return redirect('rekap_admin')
