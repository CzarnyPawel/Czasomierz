from audioop import reverse
from lib2to3.fixes.fix_input import context
from datetime import datetime, timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm, WorkLogStartTimeForm, WorkLogEndTimeForm
from .models import User, WorkLog


# Create your views here.

class LoginView(FormView):
    """User login view to the application"""
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class LogoutView(View):
    """Logout view"""

    def get(self, request):
        logout(request)
        return redirect('login')


class HomePageView(LoginRequiredMixin, TemplateView):
    """View of the home page, after the user logs in to the application"""
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context


class UserRegisterView(FormView):
    """View of the register form, after user clicks the Register button"""
    template_name = 'user_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                 last_name=lastname)
        return super().form_valid(form)


class WorkLogView(TemplateView):
    """View of the work log page, where user can do some actions"""
    template_name = 'register_time.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context


class WorkLogStartTimeView(FormView):
    template_name = 'start_time.html'
    form_class = WorkLogStartTimeForm
    success_url = reverse_lazy('worklog')

    def get_initial(self):
        initial = super().get_initial()
        initial['employee'] = self.request.user.id
        initial['start_time'] = datetime.now() + timedelta(hours=1)
        return initial

    def form_valid(self, form):
        start_time = form.cleaned_data['start_time']
        employee = self.request.user
        if WorkLog.objects.filter(employee=employee, start_time__date=start_time.date()).exists():
            form.add_error(None, "W danym dniu istnieje zarejestrowane rozpoczęcie pracy")
            return self.form_invalid(form)
        WorkLog.objects.create(employee=employee, start_time=start_time)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context


class WorkLogEndTimeView(UpdateView):
    form_class = WorkLogEndTimeForm
    model = WorkLog
    template_name = 'worklog_update_form.html'
    success_url = reverse_lazy('worklog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['employee'] = self.request.user.id
        initial['end_time'] = datetime.now() + timedelta(hours=1)

        return initial

    def get_object(self, queryset=None):
        try:
            obj = WorkLog.objects.get(employee=self.request.user, end_time__isnull=True)
        except WorkLog.DoesNotExist:
            raise WorkLog.DoesNotExist
        except WorkLog.MultipleObjectsReturned:
            raise WorkLog.MultipleObjectsReturned
        return obj

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request)
        except WorkLog.DoesNotExist:
            return redirect('/end-time404/')

        except WorkLog.MultipleObjectsReturned:
            # do obsłużenia, jeśli występuje więcej niż jedno zdarzenie w danym dniu
            return redirect('/end-time-multi/')

class WorkLogEndTime404(TemplateView):
    template_name = 'worklog404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context

class WorkLogEndTimeMulti(ListView):
    model = WorkLog
    template_name = 'worklog_multiple.html'

    def get_queryset(self):
        return WorkLog.objects.filter(employee=self.request.user, end_time__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context

class WorkLogEndTimeMultiDelete(DeleteView):
    model = WorkLog
    success_url = reverse_lazy('worklog')
    template_name = 'worklog_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context