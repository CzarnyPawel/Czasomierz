from datetime import datetime, timedelta
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

    def clean(self):
        cleaned_data =super().clean()
        start_time = cleaned_data.get('start_time')
        current_time = datetime.now() + timedelta(hours=1)


class WorkLogEndTimeForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['start_time', 'end_time', 'tasks']
        labels = {
            'end_time': 'Data i godzina zakończenia pracy',
            'tasks': 'Zrealizowane zadania',
        }

class WorkLogReportForm(forms.Form):
    start_time = forms.DateField(label='Zakres daty - od', widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.DateField(label='Zakres daty - do', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time > end_time:
            raise ValidationError('Podana data "od" nie może być większa od podanej daty "do"')
        return cleaned_data