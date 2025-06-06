# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ManualPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jenis_kelamin = models.CharField(max_length=1)
    kehamilan = models.FloatField()
    glukosa = models.FloatField()
    tekanan = models.FloatField()
    kulit = models.FloatField()
    insulin = models.FloatField()
    berat = models.FloatField()
    tinggi = models.FloatField()
    bmi = models.FloatField()
    riwayat = models.FloatField()
    usia = models.FloatField()
    hasil_persen = models.FloatField()
    hasil_risiko = models.FloatField()
    hasil_tipe = models.CharField(max_length=255)
    hasil_saran = models.TextField()
    tanggal_input = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.tanggal_input.strftime("%Y-%m-%d %H:%M")}'
