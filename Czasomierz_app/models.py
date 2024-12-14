from django.db import models
from django.contrib.auth.models import AbstractUser
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

class WorkLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    tasks = models.TextField(null=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.employee}'