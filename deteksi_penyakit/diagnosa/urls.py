from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_prediksi, name="form_prediksi"),            
    path('hasil/', views.hasil_prediksi, name="hasil_prediksi"),    
]
