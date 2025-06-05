from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Hapus semua help_text
        for field in self.fields.values():
            field.help_text = ''

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']