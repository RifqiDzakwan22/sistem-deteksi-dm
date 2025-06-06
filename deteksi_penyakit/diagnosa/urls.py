from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('form/', views.form_manual, name='form_manual'),
    path('hasil/', views.hasil_prediksi, name='hasil_prediksi'),
    path('upload/', views.form_upload, name='form_upload'),
    path('login/', auth_views.LoginView.as_view(template_name='diagnosa/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_view, name='register'),
    path('rekap-admin/', views.rekap_admin, name='rekap_admin'),
    path('daftar-pengguna/', views.daftar_pengguna, name='daftar_pengguna'),
    path('hapus-pengguna/<int:user_id>/', views.hapus_pengguna, name='hapus_pengguna'),
    path('hapus-prediksi-manual/<int:prediksi_id>/', views.hapus_prediksi_manual, name='hapus_prediksi_manual'),

]
