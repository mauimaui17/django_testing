from django.shortcuts import render, HttpResponseRedirect
from .models import Student, Violation, StudentViolation
from .forms import StudentForm
from django.contrib import messages
# Create your views here.

def homepage(request):
    return render(request, "test/home.html")
def base(request):
    return render(request, "test/base.html")
def students(request):
    all_students = Student.objects.all()
    has_students = all_students.exists()
    form = StudentForm()  
    return render(request, 'test/students.html', {
        "has_students": has_students, 
        "student_list": all_students if has_students else None,
        "form": form
    })

def add_student(request):
    if (request.method == "POST"):
        form = StudentForm(request.POST)
        if form.errors:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, "%s: %s" %(error, form.errors[error]))
            return HttpResponseRedirect('/students/')
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Added a new student.")
            return HttpResponseRedirect('/students/')
    else:
        form = StudentForm()        
        return render(request, 'test/add_student.html',{"form": form})

def view_student(request):
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id = student_id)
    minor_violations = student.get_minor_violations()
    major_violations = student.get_major_violations()
    return render(
        request, 
        'test/profile.html', 
        {
            "student":student, 
            "minor": minor_violations, 
            "major": major_violations
        }
    )