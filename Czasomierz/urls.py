"""
URL configuration for Czasomierz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Czasomierz_app import views as czas_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', czas_views.LoginView.as_view(), name='login'),
    path('logout/', czas_views.LogoutView.as_view(), name='logout'),
    path('register/', czas_views.UserRegisterView.as_view(), name='register'),
    path('', czas_views.HomePageView.as_view(), name='main'),
    path('work-time/', czas_views.WorkLogView.as_view(), name='worklog'),
    path('start-time/', czas_views.WorkLogStartTimeView.as_view(), name='start_time'),
    path('end-time/', czas_views.WorkLogEndTimeView.as_view(), name='end_time'),
    path('end-time404/', czas_views.WorkLogEndTime404.as_view(), name='worklog404'),
    path('end-time-multi/', czas_views.WorkLogEndTimeMulti.as_view()),
    path('delete-time/<int:pk>/', czas_views.WorkLogEndTimeMultiDelete.as_view(), name='delete_time'),
    path('report/', czas_views.WorkLogReportView.as_view(), name='report'),
    path('show-report/', czas_views.WorkLogReportShow.as_view(), name='show_report'),
    path('no-event/', czas_views.WorkLogNoEventView.as_view(), name='no_event'),
    path('time-correction/', czas_views.WorkLogTimeCorrectionView.as_view(), name='time_correction'),
    path('time-correction404/', czas_views.WorkLogTimCorrection404.as_view(), name='time_correction404'),
    path('time-correction-update/<int:pk>/', czas_views.WorkLogTimeCorrectionUpdateView.as_view(), name='time_correction_update'),
    path('acceptance/', czas_views.WorkLogAcceptanceView.as_view(), name='acceptance'),
    path('delete-record/<int:pk>/', czas_views.WorkLogAcceptanceDeleteView.as_view(), name='delete_record'),
    path('update-record/<int:pk>/', czas_views.WorkLogAcceptanceUpdateView.as_view(), name='update_record'),
]
