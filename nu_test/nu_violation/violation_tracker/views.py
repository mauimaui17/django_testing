from django.shortcuts import render
from .models import Student, Violation, StudentViolation
# Create your views here.

def homepage(req):
    return render(req, "test/home.html")
def base(req):
    return render(req, "test/base.html")
def students(req):
    all_students = Student.objects.all()
    has_students = all_students.exists()
    
    return render(req, 'test/students.html', {
        "has_students": has_students, 
        "student_list": all_students if has_students else None
    })