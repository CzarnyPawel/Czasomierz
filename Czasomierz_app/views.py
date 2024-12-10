from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import LoginForm
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
    def get(self, request):
        logout(request)
        return redirect('login')
class HomePageView(TemplateView):
    """View of the home page, after the user logs in to the application"""
    template_name = 'main.html'
