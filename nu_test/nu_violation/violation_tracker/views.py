from django.shortcuts import render, HttpResponseRedirect
from .models import Student, Violation, StudentViolation
from .forms import StudentForm, StudentViolationForm, StudentViolationFile
from django.contrib import messages
from datetime import datetime
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
    try:
        # Fetch the student by ID
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Student does not exist.")
        return HttpResponseRedirect('/students/')
    minor_violations = student.get_minor_violations()
    major_violations = student.get_major_violations()
    minor_form = StudentViolationForm()
    minor_form.fields["violation"].queryset = Violation.objects.all().filter(violation_class__exact = "Minor")
    major_form = StudentViolationForm()
    major_form.fields["violation"].queryset = Violation.objects.all().filter(violation_class__exact = "Major")

    return render(
        request, 
        'test/profile.html', 
        {
            "student":student, 
            "minor": minor_violations, 
            "major": major_violations,
            "minor_form": minor_form,
            "major_form": major_form
        }
    )
    
def add_student_violation(request):
    if request.method == "POST":
        form = StudentViolationForm(request.POST)
        files = request.FILES.getlist('files')  # Get the uploaded files
        student_id = request.POST.get("student_id")
        try:
            # Fetch the student by ID
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Student does not exist.")
            return HttpResponseRedirect('/students/')
        
        if form.errors:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, "%s: %s" %(error, form.errors[error]))
            return HttpResponseRedirect(f'/view-student/?student_id{student_id}')
        if form.is_valid():
            record = form.save(commit=False)
            record.student = student
            counter = 0
            similar_violations = StudentViolation.objects.filter(
                student=student, violation=record.violation
            ).count()
            record.offense_count = similar_violations + 1
            current_time = datetime.now()
            record.time = current_time
            record.save()
            for file in files:
                StudentViolationFile.objects.create(student_violation=record, file=file)

            messages.add_message(request, messages.SUCCESS, "Added a violation record.")
            return HttpResponseRedirect(f'/view-student/?student_id={student_id}')