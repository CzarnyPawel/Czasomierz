from datetime import datetime, timedelta
from logging import disable
from os.path import exists

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from workalendar.core import cleaned_date

from .models import User, TeamUser, WorkLog, OffWorkLog


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


class WorkLogStartTimeForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['start_time', 'employee']

    employee = forms.ModelChoiceField(queryset=User.objects.all(), label='Pracownik', widget=forms.HiddenInput)
    start_time = forms.DateTimeField(label="Data i godzina rozpoczęcia pracy", disabled=True)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        current_time = datetime.now() + timedelta(hours=1)


class WorkLogEndTimeForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['start_time', 'end_time', 'tasks']
        labels = {
            'tasks': 'Zrealizowane zadania',
        }

    start_time = forms.DateTimeField(label='Data i godzina rozpoczęcia pracy', disabled=True)
    end_time = forms.DateTimeField(label='Data i godzina zakończenia pracy', disabled=True)


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


class WorkLogNoEventForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['start_time', 'end_time', 'tasks']

    start_time = forms.DateTimeField(label='Godzina i data rozpoczęcia pracy',
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(label='Godzina i data zakończenia pracy',
                                   widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    tasks = forms.CharField(label='Zrealizowane zadania', widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time > end_time:
            raise ValidationError(
                'Data i godzina rozpoczęcia pracy nie może być późniejsza niż data i godzina zakończenia pracy')
        return cleaned_data


class WorkLogTimeCorrectionForm(forms.Form):
    date_field = forms.DateField(label='Data korekty czasu pracy', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        date_field = cleaned_data.get('date_field')
        if date_field is None:
            raise ValidationError('Należy podać poprawną datę')
        return cleaned_data


class WorkLogCorrectionUpdateForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['start_time', 'end_time']

    start_time = forms.DateTimeField(label='Godzina i data rozpoczęcia pracy',
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(label='Godzina i data zakończenia pracy',
                                   widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time > end_time:
            raise ValidationError(
                'Data i godzina rozpoczęcia pracy nie może być późniejsza niż data i godzina zakończenia pracy')
        if start_time is None or end_time is None:
            raise ValidationError(
                'Należy podać poprawną datę rozpoczęcia i zakończenia czasu pracy'
            )
        return cleaned_data


class OffWorkLogApplicationForm(forms.ModelForm):
    class Meta:
        model = OffWorkLog
        fields = ['start_date', 'end_date', 'name']

    name = forms.CharField(label='Rodzaj urlopu', disabled=True)
    start_date = forms.DateTimeField(label='Data rozpoczęcia urlopu', widget=forms.DateTimeInput(attrs={'type': 'date'}))
    end_date = forms.DateTimeField(label='Data zakończenia urlopu', widget=forms.DateTimeInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            raise ValidationError(
                'Data rozpoczęcia urlopu nie może być późniejsza niż data zakończenia urlopu')
        if start_date is None or end_date is None:
            raise ValidationError(
                'Należy podać poprawną datę rozpoczęcia i zakończenia urlopu'
            )
        return cleaned_data

class OffWorkLogVacationUpdateForm(forms.ModelForm):
    class Meta:
        model = OffWorkLog
        fields = ['reason']

    reason = forms.CharField(label='Uzasadnienie odrzucenia wniosku', widget=forms.Textarea)