from django.contrib import admin
from Czasomierz_app.models import User, TeamUser, Team, WorkLog, OffWorkLog, AmountOfLeave, UsedDays
# Register your models here.
admin.site.register(User)
admin.site.register(Team)
admin.site.register(TeamUser)
admin.site.register(WorkLog)
admin.site.register(OffWorkLog)
admin.site.register(AmountOfLeave)
admin.site.register(UsedDays)
