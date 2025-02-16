# Generated by Django 5.1.4 on 2025-01-08 16:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Czasomierz_app', '0005_worklog_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountOfLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('days_to_use', models.PositiveIntegerField()),
                ('used_days', models.PositiveIntegerField(default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('employee', 'year')},
            },
        ),
        migrations.CreateModel(
            name='OffWorkLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('name', models.CharField(default='Urolp wypoczynkowy', max_length=50)),
                ('status', models.CharField(choices=[('oczekuje', 'Oczekuje'), ('zaakceptowany', 'Zaakceptowany'), ('odrzucony', 'Odrzucony')], max_length=30)),
                ('reason', models.CharField(max_length=100, null=True)),
                ('amount_of_leave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Czasomierz_app.amountofleave')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
