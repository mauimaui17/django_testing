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
    # files = forms.FileField(
    #     widget=forms.FileInput(attrs={'multiple': True}), 
    #     required=False, 
    #     label="Upload files"
    # )
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
        
    # def save(self, commit=True):
    #     instance = super().save(commit=commit)
        
    #     # Check if any files were uploaded
    #     files = self.files.getlist('files')
    #     if files:
    #         for file in files:
    #             StudentViolationFile.objects.create(student_violation=instance, file=file)

    #     return instance
        