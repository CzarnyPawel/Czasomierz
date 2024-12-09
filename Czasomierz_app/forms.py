from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from .models import User

class LoginForm(forms.Form):

    username = forms.CharField(label='Nazwa użytkownika', required=True)
    password = forms.CharField(label='Hasło', widget=PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Podałeś złe hasło lub login')
        else:
            self.user = user