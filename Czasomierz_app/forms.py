from os.path import exists

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from .models import User, TeamUser, WorkLog


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

class RegisterForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', required=True)
    password = forms.CharField(label='Hasło', widget=PasswordInput, required=True)
    confirm_password = forms.CharField(label="Powtórz hasło", widget=PasswordInput, required=True)
    email = forms.EmailField(label='Adres e-mail', required=True)
    firstname = forms.CharField(label='Imię użytkownika', required=True)
    lastname = forms.CharField(label='Nazwisko użytkownika', required=True)


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if password != confirm_password:
            raise ValidationError('Podane hasła nie są jednakowe')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Podana nazwa użytkownika istnieje w systemie. Proszę podać inną nazwę.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Podany adres email istnieje w systemie. Proszę podać inny adres.")
        return cleaned_data

class WorkLogStartTimeForm(forms.Form):
    employee = forms.CharField(label='Pracownik', widget=forms.HiddenInput)
    start_time = forms.DateTimeField(label="Data i godzina rozpoczęcia pracy")