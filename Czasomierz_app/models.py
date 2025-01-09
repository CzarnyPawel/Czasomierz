from tkinter.constants import CASCADE

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from workalendar.europe import Poland
from datetime import datetime, timedelta
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    teams = models.ManyToManyField('Team', through='TeamUser')
    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    def __str__(self):
        return f'{self.name}'

class TeamUser(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('team_lead', 'Team Lead'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    class Meta:
        unique_together = ('user', 'team')
    def __str__(self):
        return f'{self.user} - {self.team} - {self.role}'

class WorkLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    tasks = models.TextField(null=True)
    state = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default='Rejestracja czasu pracy')
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.employee}'

class AmountOfLeave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    days_to_use = models.PositiveIntegerField()
    class Meta:
        unique_together = ('employee', 'year')

    def __str__(self):
        return f'{self.employee.first_name}, year: {self.year}, days: {self.days_to_use}'

class OffWorkLog(models.Model):
    STATUS_CHOICES = [
        ('oczekuje', 'Oczekuje'),
        ('zaakceptowany', 'Zaakceptowany'),
        ('odrzucony', 'Odrzucony'),
    ]
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=50, default='Urolp wypoczynkowy')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='oczekuje')
    reason = models.CharField(max_length=100, blank=True, null=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_of_leave = models.ForeignKey(AmountOfLeave, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.employee.first_name}, {self.start_date} - {self.end_date}'

class UsedDays(models.Model):
    used_days = models.PositiveIntegerField(default=0)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.employee.first_name}, {self.used_days}'