from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import HomeView, FormManualView, UserLoginView, HasilPrediksiView, UploadCSVView, LogoutUserView, RegisterView, RekapAdminView, DaftarPenggunaView,  HapusPenggunaView, HapusPrediksiManualView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('form/', FormManualView.as_view(), name='form_manual'),
    path('hasil/', HasilPrediksiView.as_view(), name='hasil_prediksi'),
    path('upload/', UploadCSVView.as_view(), name='form_upload'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('rekap-admin/', RekapAdminView.as_view(), name='rekap_admin'),
    path('daftar-pengguna/', DaftarPenggunaView.as_view(), name='daftar_pengguna'),
    path('hapus-pengguna/<int:user_id>/', HapusPenggunaView.as_view(), name='hapus_pengguna'),
    path('hapus-prediksi-manual/<int:prediksi_id>/', HapusPrediksiManualView.as_view(), name='hapus_prediksi_manual'),
]