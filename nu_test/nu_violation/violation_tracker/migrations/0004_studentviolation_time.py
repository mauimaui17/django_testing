# Generated by Django 4.2.15 on 2024-09-22 06:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation_tracker', '0003_studentviolation_status_studentviolationfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentviolation',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 22, 14, 52, 37, 301127)),
        ),
    ]
