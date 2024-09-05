from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from datetime import datetime
import random
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
        blank=True
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
        blank=True 
    )
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    def get_minor_count(self):
        return self.violations.all().filter(violation__violation_class="Minor").count()
    def get_major_count(self):
        return self.violations.all().filter(violation__violation_class="Major").count()


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

    def __str__(self):
        return f"{self.student} - {self.violation}"
