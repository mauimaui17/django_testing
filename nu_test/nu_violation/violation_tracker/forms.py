from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name", 
            "last_name",
            "student_id",
            "enrollment_year",
            "grade_level",
            "strand"
        ]
        labels = {            
            "first_name": "First Name",
            "last_name": "Last Name",
            "student_id":"Student ID",
            "enrollment_year":"Enrollment Year",
            "grade_level":"Grade Level",
            "strand":"Strand",
            }
            
class StudentViolationForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        (1, 'Category 1'),
        (2, 'Category 2'),
        (3, 'Category 3'),
    ]
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Category/Intervention")

    class Meta:
        model = StudentViolation
        fields = [
            "violation",
            "category",
            "status",
            "remarks"
        ]
        labels = {
            "category": "Category/Intervention",
            "status": "Resolved"
        }

class ViolationForm(forms.ModelForm):
    class Meta:
        model = Violation
        fields = [
            "title",
        ]
        labels = {
            "title": "Violation Title",
        }
