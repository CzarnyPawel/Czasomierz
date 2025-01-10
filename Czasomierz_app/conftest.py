import pytest
from django.contrib.auth import get_user_model

from .models import User, Team, TeamUser
from django.test import Client


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def create_user():
    user = User.objects.create_user(username='test', password='test')
    return user


@pytest.fixture
def create_user_with_another_roles():
    team1 = Team.objects.create(name='Dział rozwoju', description='Dział odpowiedzialny za rozwój')
    team2 = Team.objects.create(name='Dział inwestycji', description='Dział odpowiedzialny za inwestycje')

    employee1 = User.objects.create_user(username='employee1', password='test', email='employee1@test.com')
    employee2 = User.objects.create_user(username='employee2', password='test', email='employee2@test.com')
    team_lead1 = User.objects.create_user(username='team_lead1', password='test', email='team_lead1@test.com')
    team_lead2 = User.objects.create_user(username='team_lead2', password='test', email='team_lead2@test.com')

    TeamUser.objects.create(user=employee1, team=team1, role='employee')
    TeamUser.objects.create(user=employee2, team=team2, role='employee')
    TeamUser.objects.create(user=team_lead1, team=team1, role='team_lead')
    TeamUser.objects.create(user=team_lead2, team=team2, role='team_lead')

    return team1, team2, employee1, employee2, team_lead1, team_lead2


@pytest.fixture
def create_user_model():
    # pobieram aktualny model użytkownika, aby móc tworzyć nowych użytkowników
    User = get_user_model()
    return User


@pytest.fixture
def create_user_no_team_lead():
    team = Team.objects.create(name='Dział finansów', description='Dział odpowiedzialny za finanse')
    employee5 = User.objects.create_user(username='employee5', password='test', email='employee@test.com')
    TeamUser.objects.create(user=employee5, team=team, role='employee')
    return team, employee5
