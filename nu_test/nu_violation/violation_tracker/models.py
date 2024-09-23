from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from datetime import datetime
import random
import os
from uuid import uuid4

# Create your models here.

class Violation(models.Model):
    VIOLATION_CLASSES = [
        ("Minor", "Minor"),
        ("Major", "Major"),
    ]
    title = models.CharField(
        max_length=200, 
        default=""
    )
    violation_class = models.CharField(
        max_length=200, 
        choices=VIOLATION_CLASSES, 
        default="Minor"
    )
    def __str__(self):
        return self.title

class Student(models.Model):
    
    first_name = models.CharField(
        max_length=200, 
        default="")
    last_name = models.CharField(
        max_length=200, 
        default="")
    student_id = models.CharField(
        max_length=12, 
        unique=True, 
        validators=[
            RegexValidator(
                regex=r'20[0-9]{2}-[0-9]{6}', 
                message="Please input a valid student ID in the format 20XX-XXXXXX", 
                code="invalid_student_id"
            )
        ],
        blank=False
    )
    enrollment_year = models.IntegerField(
        validators=[
            MaxValueValidator(datetime.now().year),
            MinValueValidator(2000)
        ]
    )
    GRADE_LEVEL_CHOICES = [
        ("SHS11", "Grade 11"),
        ("SHS12", "Grade 12"),
        ("COLG1", "First Year College"),
        ("COLG2", "Second Year College"),
        ("COLG3", "Third Year College"),
        ("COLG4", "Fourth Year College")
        ]

    grade_level = models.CharField(
        max_length=200, 
        choices=GRADE_LEVEL_CHOICES, 
        blank=False
    )
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    def get_minor_count(self):
        return self.violations.all().filter(violation__violation_class="Minor").count()
    def get_major_count(self):
        return self.violations.all().filter(violation__violation_class="Major").count()
    def get_minor_violations(self):
        return self.violations.all().filter(violation__violation_class="Minor")
    def get_major_violations(self):
        return self.violations.all().filter(violation__violation_class="Major")


class StudentViolation(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name="violations"
    )
    violation = models.ForeignKey(
        Violation, 
        on_delete=models.CASCADE
    )
    offense_count = models.IntegerField(
        default=1, 
        validators=[
            MaxValueValidator(3), 
            MinValueValidator(1)
        ]
    )
    category = models.IntegerField(
        default=1, 
        validators=[
            MaxValueValidator(5), 
            MinValueValidator(1)
        ]
    )
    remarks = models.CharField(blank=True)
    status = models.BooleanField(default=False)
    time = models.DateTimeField(blank=True, default=datetime.now())
    def __str__(self):
        return f"{self.student} - {self.violation}"

def student_violation_file_path(instance, filename):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d")
    return os.path.join(f"violations/student_{instance.student_violation.student.student_id}/{instance.student_violation.violation.title}/{formatted_time}", filename)

class StudentViolationFile(models.Model):
    student_violation = models.ForeignKey(StudentViolation, on_delete=models.CASCADE, related_name="violation_files")
    file = models.FileField(upload_to=student_violation_file_path)

    def __str__(self):
        return f"File for {self.student_violation}"