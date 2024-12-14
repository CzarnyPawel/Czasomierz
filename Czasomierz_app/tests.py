import pytest
from django.urls import reverse_lazy, reverse

from .models import User

# Create your tests here.
@pytest.mark.django_db
def test_login_view(client):
    response = client.post('/login/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_view_correct_data(client):
    User.objects.create_user(username='test', password='test')
    data = {
        'username': 'test',
        'password': 'test'
    }
    url = reverse('login')
    response = client.post(url, data, follow =True)
    assert response.context['user'].username == 'test'
    #response = client.login(username='test', password='test')
    #assert response



@pytest.mark.django_db
def test_logout_view(client):
    User.objects.create_user(username='test', password='test')
    client.login(username='test', password='test')
    url = reverse('logout')
    response = client.get(url, follow =True)
    assert not response.context['user'].username == 'test'

@pytest.mark.django_db
def test_login_view_redirect_after_login(client):
    User.objects.create_user(username='test', password='test')
    response = client.post('/login/', {'username': 'test', 'password': 'test'})
    assert response.status_code == 302
    assert response.url == '/'

@pytest.mark.django_db
def test_homepage_view(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'main.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_user_register_view(client):
    response = client.get('/register/')
    assert response.status_code == 200
    assert 'user_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_user_register_view_user_exists(client):
    form_data = {
        'username': 'Jan',
        'firstname': 'Jan',
        'lastname': 'Kowalski',
        'email': 'test@test.pl',
        'password': 'test',
        'confirm_password': 'test',
    }
    response = client.post('/register/', form_data)
    assert User.objects.get(username='Jan')
    assert response.status_code == 302

