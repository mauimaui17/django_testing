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
            "grade_level"
        ]
        labels = {            
            "first_name": "First Name",
            "last_name": "Last Name",
            "student_id":"Student ID",
            "enrollment_year":"Enrollment Year",
            "grade_level":"Grade Level"}
            
class StudentViolationForm(forms.ModelForm):
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
