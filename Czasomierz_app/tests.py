from datetime import datetime, timedelta
from django.utils.timezone import now
import pytest
from django.core import mail
from django.urls import reverse
from .models import User, WorkLog, AmountOfLeave, UsedDays, OffWorkLog


# Create your tests here.
@pytest.mark.django_db
def test_login_view(client):
    response = client.post('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_correct_data(client, create_user):
    data = {
        'username': 'test',
        'password': 'test'
    }
    url = reverse('login')
    response = client.post(url, data, follow=True)
    assert response.context['user'].username == 'test'


@pytest.mark.django_db
def test_logout_view(client, create_user):
    client.login(username='test', password='test')
    url = reverse('logout')
    response = client.get(url, follow=True)
    assert not response.context['user'].username == 'test'


@pytest.mark.django_db
def test_login_view_redirect_after_login(client, create_user):
    response = client.post('/login/', {'username': 'test', 'password': 'test'})
    assert response.status_code == 302
    assert response.url == '/'


@pytest.mark.django_db
def test_homepage_view(client, create_user_with_another_roles):
    response = client.post('/login/', {'username': 'employee1', 'password': 'test'})
    assert response.status_code == 302
    assert response.url == '/'
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


@pytest.mark.django_db
def test_worklog_view(client, create_user_with_another_roles):
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    response = client.get('/work-time/')
    assert response.status_code == 200
    assert 'register_time.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_worklog_start_time_view(client, create_user_with_another_roles):
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    response = client.get('/start-time/')
    assert response.context['start_time'] <= datetime.now() + timedelta(hours=1, minutes=1)
    assert response.status_code == 200
    assert 'start_time.html' in [t.name for t in response.templates]
    assert 'form' in response.context


@pytest.mark.django_db
def test_worklog_end_time_redirect_on_does_not_exist(client, create_user_with_another_roles):
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    response = client.get('/end-time/')
    assert response.status_code == 302
    assert response.url == '/end-time404/'


@pytest.mark.django_db
def test_worklog_end_time_returned_multi_object(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    start_time = now()
    WorkLog.objects.create(employee=employee1, start_time=start_time, end_time=None)
    WorkLog.objects.create(employee=employee1, start_time=start_time, end_time=None)
    response = client.get(reverse('end_time'))
    assert response.status_code == 302
    assert response.url == '/end-time-multi/'


@pytest.mark.django_db
def test_worklog_end_time_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    start_time = now()
    WorkLog.objects.create(employee=employee1, start_time=start_time, end_time=None)
    end_time = now()
    response = client.post('/end-time/', {'end_time': end_time, 'tasks': 'test'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_worklog_end_time_404_view(client, create_user_with_another_roles):
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    response = client.get('/end-time404/')
    assert response.status_code == 200
    assert 'worklog404.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_worklog_end_time_multi_view(client, create_user_with_another_roles):
    client.post('/login/', {'username': 'team_lead1', 'password': 'test'})
    response = client.get('/end-time-multi/')
    assert response.status_code == 200
    assert 'worklog_multiple.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_worklog_end_time_multi_delete(client, create_user_model, create_user_with_another_roles):
    user3 = User.objects.create_user(username='employee3', password='test')
    client.post('/login/', {'username': 'employee3', 'password': 'test'})
    start_time = now()
    obj1 = WorkLog.objects.create(employee=user3, start_time=start_time, end_time=None)
    obj2 = WorkLog.objects.create(employee=user3, start_time=start_time, end_time=None)
    client.post(f'/delete-time/{obj1.id}/')
    assert WorkLog.objects.filter(id=obj1.id).exists() == False
    client.logout()
    client.post('/login/', {'username': 'employee2', 'password': 'test'})
    response = client.post(f'/delete-time/{obj2.id}/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_worklog_show_report_view(client, create_user_with_another_roles):
    client.post('/login/', {'username': 'employee2', 'password': 'test'})
    start_time = now()
    start_date = start_time.date().isoformat()
    end_time = now() + timedelta(days=5)
    end_date = end_time.date().isoformat()
    response = client.post('/report/', {'start_time': start_date, 'end_time': end_date})
    assert response.status_code == 302
    assert response.url == '/show-report/'
    response = client.get('/show-report/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_worklog_no_event_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'team_lead2', 'password': 'test'})
    response = client.get('/no-event/')
    assert response.status_code == 200
    start_time = now()
    end_time = now() + timedelta(hours=8)
    WorkLog.objects.create(employee=team_lead2, start_time=start_time, end_time=end_time, state=True, tasks='test',
                           name='test')
    response = client.post('/no-event/', {'start_time': start_time, 'end_time': end_time, 'tasks': 'test'})
    assert WorkLog.objects.filter(employee=team_lead2, start_time__date=start_time, end_time__date=end_time)
    assert 'W danym dniu istnieje zarejestrowane rozpoczęcie i zakończenie czasu pracy' in response.context[
        'form'].non_field_errors()
    assert len(WorkLog.objects.filter(employee=team_lead2)) == 1
    response = client.post('/no-event/',
                           {'start_time': start_time + timedelta(days=1), 'end_time': end_time + timedelta(days=1),
                            'tasks': 'test'})
    assert response.status_code == 302
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_worklog_time_correction_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'team_lead2', 'password': 'test'})
    response = client.get('/time-correction/')
    assert response.status_code == 200
    response = client.post('/time-correction/')
    assert 'Należy podać poprawną datę' in response.context['form'].non_field_errors()
    date_time = now()
    date_field = date_time.date().isoformat()
    WorkLog.objects.create(employee=team_lead2, start_time=date_time, end_time=date_time + timedelta(hours=8),
                           state=True, tasks='test',
                           name='test')
    WorkLog.objects.create(employee=team_lead2, start_time=date_time + timedelta(days=5),
                           end_time=date_time + timedelta(days=6),
                           state=True, tasks='test',
                           name='test')
    response = client.post('/time-correction/', {'date_field': date_field})
    assert WorkLog.objects.filter(employee=team_lead2, start_time__date=date_time,
                                  end_time__date=date_time + timedelta(hours=8))
    assert response.status_code == 302
    date_time = now() + timedelta(days=5)
    date_field = date_time.date().isoformat()
    response = client.post('/time-correction/', {'date_field': date_field})
    assert WorkLog.objects.filter(employee=team_lead2, start_time__date__gte=date_time,
                                  end_time__date__lte=date_time + timedelta(days=1)).first()
    assert response.status_code == 302
    date_time = now() + timedelta(days=2)
    date_field = date_time.date().isoformat()
    response = client.post('/time-correction/', {'date_field': date_field})
    assert 'Wyszukanie rekordu do wniosku o korektę czasu pracy jest niemożliwe, ponieważ dla wskazanej daty nie istnieje zarejestrowany czas pracy.' in \
           response.context['form'].non_field_errors()


@pytest.mark.django_db
def test_worklog_time_correction_update_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'employee2', 'password': 'test'})
    date_time = now()
    obj = WorkLog.objects.create(employee=employee2, start_time=date_time, end_time=date_time + timedelta(hours=8),
                                 state=True, tasks='test',
                                 name='test')
    print(obj.id, obj.state)
    assert WorkLog.objects.filter(id=obj.id, state=True).exists() == True
    response = client.post(f'/time-correction-update/{obj.id}/',
                           {'start_time': date_time + timedelta(hours=2), 'end_time': date_time + timedelta(hours=10)})
    assert response.status_code == 302
    assert WorkLog.objects.filter(id=obj.id, state=False, name='Korekta czasu pracy').exists() == True
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_worklog_time_correction_email(client, create_user_no_team_lead):
    team, employee5 = create_user_no_team_lead
    client.post('/login/', {'username': 'employee5', 'password': 'test'})
    date_time = now()
    obj = WorkLog.objects.create(employee=employee5, start_time=date_time, end_time=date_time + timedelta(hours=8),
                                 state=True, tasks='test',
                                 name='test')
    response = client.post(f'/time-correction-update/{obj.id}/',
                           {'start_time': date_time + timedelta(hours=2), 'end_time': date_time + timedelta(hours=10)})
    assert "W zespole do którego należy użytkownik nie zdefiniowano przełożonego. Należy skontaktować się z działem kadr" in \
           response.context['form'].non_field_errors()
    assert response.status_code == 200


@pytest.mark.django_db
def test_worklog_acceptance_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'team_lead2', 'password': 'test'})
    date_time = now()
    record1 = WorkLog.objects.create(employee=employee2, start_time=date_time, end_time=date_time + timedelta(hours=8),
                                     state=False, tasks='test',
                                     name='test')
    response = client.get('/acceptance/')
    assert response.status_code == 200
    assert record1 in response.context['object_list']


@pytest.mark.django_db
def test_worklog_acceptance_delete_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'team_lead1', 'password': 'test'})
    date_time = now()
    obj = WorkLog.objects.create(employee=employee1, start_time=date_time, end_time=date_time + timedelta(hours=8),
                                 state=False, tasks='test',
                                 name='test')
    assert WorkLog.objects.filter(id=obj.id).exists() == True
    response = client.post(reverse('delete_record', args=[obj.id]))
    assert WorkLog.objects.filter(id=obj.id).exists() == False
    assert response.status_code == 302


@pytest.mark.django_db(transaction=True)
def test_worklog_acceptance_update_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'team_lead2', 'password': 'test'})
    date_time = now()
    obj = WorkLog.objects.create(employee=employee2, start_time=date_time, end_time=date_time + timedelta(hours=8),
                                 state=False, tasks='test',
                                 name='test')
    assert WorkLog.objects.filter(id=obj.id, state=False).exists() == True
    response = client.get(reverse('update_record', args=[obj.id]))
    assert WorkLog.objects.filter(id=obj.id, state=True).exists() == True
    assert response.status_code == 302


@pytest.mark.django_db
def test_off_worklog_view(client, create_user_with_another_roles):
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    response = client.get(reverse('offworklog'))
    assert response.status_code == 200
    assert 'offworklog.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_off_worklog_application_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'employee1', 'password': 'test'})
    AmountOfLeave.objects.create(employee=employee1, year=2024, days_to_use=25)
    AmountOfLeave.objects.create(employee=employee1, year=2025, days_to_use=25)
    UsedDays.objects.create(employee=employee1, used_days=10)
    response = client.get(reverse('application'))
    assert response.context['days'] == 40
    assert response.context['days_outstanding'] == 15
    response = client.post('/application/', {'start_date': now().date() + timedelta(days=1), 'end_date': now().date()})
    assert 'Data rozpoczęcia urlopu nie może być późniejsza niż data zakończenia urlopu' in response.context[
        'form'].non_field_errors()
    response = client.post('/application/',
                           {'start_date': now().date(), 'end_date': now().date() + timedelta(days=59)})
    assert 'Brak wystarczającej ilości urlopu' in response.context['form'].non_field_errors()
    amount_of_leave = AmountOfLeave.objects.filter(employee=employee1).first()
    OffWorkLog.objects.create(employee=employee1, start_date=now(), end_date=now() + timedelta(days=3),
                              amount_of_leave=amount_of_leave)
    response = client.post('/application/',
                           {'start_date': now().date() + timedelta(days=1),
                            'end_date': now().date() + timedelta(days=2)})
    assert 'W podanym okresie istnieje już złożony wniosek o urlop' in response.context['form'].non_field_errors()
    response = client.post('/application/',
                           {'start_date': now().date() + timedelta(days=7),
                            'end_date': now().date() + timedelta(days=8)})
    assert response.status_code == 302
    assert UsedDays.objects.get(employee=employee1).used_days == 11
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_off_worklog_report_show(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    client.post('/login/', {'username': 'employee2', 'password': 'test'})
    AmountOfLeave.objects.create(employee=employee2, year=2025, days_to_use=25)
    UsedDays.objects.create(employee=employee2, used_days=10)
    amount_of_leave = AmountOfLeave.objects.filter(employee=employee2).first()
    record1 = OffWorkLog.objects.create(employee=employee2, start_date=now(), end_date=now() + timedelta(days=3),
                                        amount_of_leave=amount_of_leave)
    response = client.get(reverse('vacation_report'))
    assert response.status_code == 200
    assert record1 in response.context['object_list']
    assert 'offworklog_report_show.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_off_worklog_acceptance_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    AmountOfLeave.objects.create(employee=employee1, year=2025, days_to_use=18)
    UsedDays.objects.create(employee=employee1, used_days=10)
    amount_of_leave = AmountOfLeave.objects.filter(employee=employee1).first()
    record1 = OffWorkLog.objects.create(employee=employee1, start_date=now(), end_date=now() + timedelta(days=3),
                                        amount_of_leave=amount_of_leave)
    client.post('/login/', {'username': 'team_lead1', 'password': 'test'})
    response = client.get(reverse('vacation-acceptance'))
    assert response.status_code == 200
    assert record1 in response.context['object_list']
    client.post('/login/', {'username': 'team_lead2', 'password': 'test'})
    response = client.get(reverse('vacation-acceptance'))
    assert not record1 in response.context['object_list']


@pytest.mark.django_db
def test_off_worklog_acceptance_update_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    AmountOfLeave.objects.create(employee=employee2, year=2025, days_to_use=15)
    UsedDays.objects.create(employee=employee2, used_days=5)
    amount_of_leave = AmountOfLeave.objects.filter(employee=employee2).first()
    record1 = OffWorkLog.objects.create(employee=employee2, start_date=now(), end_date=now() + timedelta(days=3),
                                        amount_of_leave=amount_of_leave, status='oczekuje')
    client.post('/login/', {'username': 'team_lead2', 'password': 'test'})
    assert OffWorkLog.objects.filter(id=record1.id, status='zaakceptowany').exists() == False
    client.get(reverse('update_vacation', args=[record1.id]))
    assert OffWorkLog.objects.filter(id=record1.id, status='zaakceptowany').exists()


@pytest.mark.django_db
def test_off_worklog_vacation_rejected_update_view(client, create_user_with_another_roles):
    team1, team2, employee1, employee2, team_lead1, team_lead2 = create_user_with_another_roles
    AmountOfLeave.objects.create(employee=employee2, year=2025, days_to_use=26)
    UsedDays.objects.create(employee=employee2, used_days=17)
    amount_of_leave = AmountOfLeave.objects.filter(employee=employee2).first()
    record1 = OffWorkLog.objects.create(employee=employee2, start_date=now(), end_date=now() + timedelta(days=2),
                                        amount_of_leave=amount_of_leave, status='oczekuje')
    client.post('/login/', {'username': 'team_lead2', 'password': 'test'})
    assert OffWorkLog.objects.filter(id=record1.id, status='odrzucony').exists() == False
    response = client.post(f'/update-reject/{record1.id}/', {'reason': 'test'})
    assert UsedDays.objects.get(employee=employee2).used_days == 16
    assert OffWorkLog.objects.filter(id=record1.id, status='odrzucony', reason='test').exists()
    assert response.status_code == 302
