from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_prediksi, name='form_prediksi'),
    path('hasil/', views.hasil_prediksi, name='hasil_prediksi'),
    path('login/', auth_views.LoginView.as_view(template_name='diagnosa/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
