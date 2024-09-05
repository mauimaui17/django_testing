# Generated by Django 4.2.15 on 2024-09-04 13:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation_tracker', '0002_student_grade_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(blank=True, max_length=12, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_student_id', message='Please input a valid student ID in the format 20XX-XXXXXX', regex='20[0-9]{2}-[0-9]{6}')]),
        ),
    ]
