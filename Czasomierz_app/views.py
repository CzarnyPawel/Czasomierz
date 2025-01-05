from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from .forms import LoginForm, RegisterForm, WorkLogStartTimeForm, WorkLogEndTimeForm, WorkLogReportForm, \
    WorkLogNoEventForm, WorkLogTimeCorrectionForm, WorkLogCorrectionUpdateForm
from .models import User, WorkLog, TeamUser
from datetime import datetime, date, time, timedelta
from django.core.mail import EmailMultiAlternatives


# Create your views here.

class BaseContextData:
    """Base class for the context_data method"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
        return context


class LoginView(FormView):
    """User login view to the application"""
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        """Method for user login and redirection"""
        login(self.request, form.user)
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return super().form_valid(form)


class LogoutView(View):
    """Logout view"""

    def get(self, request):
        """Logout method"""
        logout(request)
        return redirect('login')


class HomePageView(LoginRequiredMixin, BaseContextData, TemplateView):
    """View of the home page, after the user logs in to the application"""
    template_name = 'main.html'


class UserRegisterView(FormView):
    """View of the register form, after user clicks the Register button"""
    template_name = 'user_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Overriding the form_valid method for registering a new user"""
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                 last_name=lastname)
        return super().form_valid(form)


class WorkLogView(LoginRequiredMixin, TemplateView):
    """View of the work log page, where user can do some actions"""
    template_name = 'register_time.html'

    def get_context_data(self, **kwargs):
        """Method for passing data to the context"""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['greeting'] = f"{self.request.user.first_name}"
            context['role'] = TeamUser.objects.get(user=self.request.user).role
        return context


class WorkLogStartTimeView(LoginRequiredMixin, BaseContextData, FormView):
    """A view where the employee can register the start time of work on the form"""
    template_name = 'start_time.html'
    form_class = WorkLogStartTimeForm
    success_url = reverse_lazy('worklog')

    def get_initial(self):
        """Method for passing initial data to the form"""
        initial = super().get_initial()
        initial['employee'] = self.request.user.id
        initial['start_time'] = datetime.now() + timedelta(hours=1)
        return initial

    def form_valid(self, form):
        """A method of filtering data and creating new objects in the database"""
        start_time = form.cleaned_data['start_time']
        employee = self.request.user
        if WorkLog.objects.filter(employee=employee, start_time__date=start_time.date()).exists():
            form.add_error(None, "W danym dniu istnieje zarejestrowane rozpoczęcie pracy")
            return self.form_invalid(form)
        WorkLog.objects.create(employee=employee, start_time=start_time)
        return super().form_valid(form)


class WorkLogEndTimeView(LoginRequiredMixin, BaseContextData, UpdateView):
    """A view where the employee can register the end time of work on the form"""
    form_class = WorkLogEndTimeForm
    model = WorkLog
    template_name = 'worklog_update_form.html'
    success_url = reverse_lazy('worklog')

    def get_initial(self):
        """Method for passing initial data to the form"""
        initial = super().get_initial()
        initial['employee'] = self.request.user.id
        initial['end_time'] = datetime.now() + timedelta(hours=1)

        return initial

    def get_object(self, queryset=None):
        """A method that handles retrieving an object from the database and exceptions"""
        try:
            obj = WorkLog.objects.get(employee=self.request.user, end_time__isnull=True)
        except WorkLog.DoesNotExist:
            raise WorkLog.DoesNotExist
        except WorkLog.MultipleObjectsReturned:
            raise WorkLog.MultipleObjectsReturned
        return obj

    def dispatch(self, request, *args, **kwargs):
        """A method that handles exceptions"""
        try:
            return super().dispatch(request)
        except WorkLog.DoesNotExist:
            return redirect('/end-time404/')

        except WorkLog.MultipleObjectsReturned:
            # do obsłużenia, jeśli występuje więcej niż jedno zdarzenie w danym dniu
            return redirect('/end-time-multi/')


class WorkLogEndTime404(LoginRequiredMixin, BaseContextData, TemplateView):
    """View showing run time end error"""
    template_name = 'worklog404.html'


class WorkLogEndTimeMulti(LoginRequiredMixin, BaseContextData, ListView):
    """A view showing a multiple object return exception"""
    model = WorkLog
    template_name = 'worklog_multiple.html'

    def get_queryset(self):
        """A method of filtering data"""
        return WorkLog.objects.filter(employee=self.request.user, end_time__isnull=True)


class WorkLogEndTimeMultiDelete(LoginRequiredMixin, UserPassesTestMixin, BaseContextData, DeleteView):
    """View showing multiple object return exception - deleting selected one"""
    model = WorkLog
    success_url = reverse_lazy('worklog')
    template_name = 'worklog_delete.html'

    def test_func(self):
        """A method that tests comparsion"""
        obj = self.get_object()
        return self.request.user == obj.employee


class WorkLogReportView(LoginRequiredMixin, BaseContextData, FormView):
    """View showing report preparation"""
    form_class = WorkLogReportForm
    template_name = 'worklog_report.html'
    success_url = reverse_lazy('show_report')

    def form_valid(self, form):
        """The method for sending data in a session"""
        self.request.session['start_time'] = str(form.cleaned_data['start_time'])
        self.request.session['end_time'] = str(form.cleaned_data['end_time'])
        return super().form_valid(form)


class WorkLogReportShow(LoginRequiredMixin, BaseContextData, ListView):
    """A view showing the report"""
    model = WorkLog
    template_name = 'worklog_report_show.html'
    context_object_name = 'objects'

    def get_queryset(self):
        """A method of filtering data from the database"""
        start_time = self.request.session.get('start_time')
        end_time = self.request.session.get('end_time')

        if start_time and end_time:
            return WorkLog.objects.filter(employee=self.request.user, start_time__date__gte=start_time,
                                          end_time__date__lte=end_time, state=True).order_by('start_time')
        return WorkLog.objects.none()


class WorkLogNoEventView(LoginRequiredMixin, BaseContextData, CreateView):
    """View showing the no event form"""
    form_class = WorkLogNoEventForm
    template_name = 'worklog_no_event.html'
    success_url = reverse_lazy('worklog')

    def form_valid(self, form):
        """A method of filtering data, creating new object and sending an e-mail"""
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        tasks = form.cleaned_data['tasks']
        if start_time and end_time and tasks:
            if WorkLog.objects.filter(employee=self.request.user, start_time__date=start_time.date(),
                                      end_time__date=end_time.date()).exists():
                form.add_error(None, "W danym dniu istnieje zarejestrowane rozpoczęcie i zakończenie czasu pracy")
                return self.form_invalid(form)
            WorkLog.objects.create(start_time=start_time, end_time=end_time, tasks=tasks, state=False,
                                   name='Brak zdarzenia',
                                   employee=self.request.user)

            user_team = self.request.user.teams.all()
            team_lead = TeamUser.objects.filter(team__in=user_team, role='team_lead')
            if team_lead.exists():
                team_lead_email = team_lead.first().user.email
            else:
                form.add_error(None,
                               "W zespole do którego należy użytkownik nie zdefiniowano przełożonego. Należy skontaktować się z działem kadr")
                return self.form_invalid(form)

            subject = 'Czasomierz: Wniosek - brak zdarzenia'
            from_email = 'czasomierz.info@gmail.com'
            to = team_lead_email
            text_content = 'W aplikacji Czasomierz w zakładce Akceptacje oczekuje nowy wniosek o brak zdarzenia.'
            html_content = '<p>W aplikacji Czasomierz w zakładce Akceptacje oczekuje nowy wniosek o brak zdarzenia</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

        return HttpResponseRedirect(self.success_url)


class WorkLogTimeCorrectionView(LoginRequiredMixin, BaseContextData, FormView):
    """A view that retrives data from database"""
    form_class = WorkLogTimeCorrectionForm
    template_name = 'worklog_time_correction.html'
    success_url = reverse_lazy('time_correction')

    def form_valid(self, form):
        """A method that retrives daa from the database, redirects to UpdateView, and handles if blocks"""
        date_field = form.cleaned_data['date_field']
        if not date_field:
            form.add_error(None, 'Należy podać poprawną datę')
            return self.form_invalid(form)
        work_log_record = WorkLog.objects.filter(
            employee=self.request.user).filter(
            Q(start_time__date=date_field, end_time__date=date_field) |
            Q(start_time__date__gte=date_field, end_time__date__lte=date_field + timedelta(days=1))).first()
        if work_log_record is None:
            form.add_error(None,
                           'Wyszukanie rekordu do wniosku o korektę czasu pracy jest niemożliwe, ponieważ dla wskazanej daty nie istnieje zarejestrowany czas pracy.')
            return self.form_invalid(form)
        return redirect(reverse('time_correction_update', kwargs={'pk': work_log_record.pk}))


class WorkLogTimCorrection404(LoginRequiredMixin, BaseContextData, TemplateView):
    """View showing time correction error"""
    template_name = 'time_correction404.html'


class WorkLogTimeCorrectionUpdateView(LoginRequiredMixin, UserPassesTestMixin, BaseContextData, UpdateView):
    """View showing update of time correction"""
    model = WorkLog
    form_class = WorkLogCorrectionUpdateForm
    template_name = 'worklog_correction_update.html'
    success_url = reverse_lazy('worklog')

    def test_func(self):
        """A method that tests comparsion"""
        obj = self.get_object()
        return self.request.user == obj.employee

    def get_initial(self):
        """Method for passing initial data to the form"""
        initial = super().get_initial()
        worklog = self.get_object()
        initial['start_time'] = worklog.start_time.strftime('%Y-%m-%dT%H:%M')
        initial['end_time'] = worklog.end_time.strftime('%Y-%m-%dT%H:%M')
        return initial

    def form_valid(self, form):
        """Method for changing the flag in the status field"""
        form.instance.state = False
        form.instance.name = 'Korekta czasu pracy'
        return super().form_valid(form)


class WorkLogAcceptanceView(LoginRequiredMixin, UserPassesTestMixin, BaseContextData, ListView):
    """View showing records of employees to be approved or denied by team_lead"""
    model = WorkLog
    template_name = 'worklog_acceptance.html'

    def test_func(self):
        """A method that tests comparsion"""
        user_role = TeamUser.objects.get(user=self.request.user)
        return user_role.role == 'team_lead'

    def get_queryset(self):
        """A method of filtering data from the database"""
        user_team = TeamUser.objects.filter(user=self.request.user).values_list('team', flat=True)
        return WorkLog.objects.filter(state=False, employee__teamuser__team__in=user_team)


class WorkLogAcceptanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, BaseContextData, DeleteView):
    """View showing entries to reject"""
    model = WorkLog
    success_url = reverse_lazy('acceptance')
    template_name = 'worklog_acceptance_delete.html'

    def test_func(self):
        """A method that tests comparsion"""
        user_role = TeamUser.objects.get(user=self.request.user)
        return user_role.role == 'team_lead'


class WorkLogAcceptanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, BaseContextData, UpdateView):
    """A view that commits a record"""
    model = WorkLog
    fields = ['state', 'start_time', 'end_time', 'employee', 'tasks']
    success_url = reverse_lazy('acceptance')
    template_name = 'worklog_acceptance_update.html'

    def test_func(self):
        """A method that tests comparsion"""
        user_role = TeamUser.objects.get(user=self.request.user)
        return user_role.role == 'team_lead'

    def get(self, request, *args, **kwargs):
        """A method that changes the flag in the state field without user action"""
        self.object = self.get_object()
        self.object.state = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
