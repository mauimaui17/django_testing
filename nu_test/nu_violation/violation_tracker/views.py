from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from .models import Student, Violation, StudentViolation
from .forms import StudentForm, StudentViolationForm, StudentViolationFile, ViolationForm
from django.contrib import messages
from datetime import datetime
from io import BytesIO
import os
import zipfile
from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):
    return render(request, "test/home.html")
def base(request):
    return render(request, "test/base.html")

@login_required
def students(request):
    all_students = Student.objects.all()
    has_students = all_students.exists()
    form = StudentForm()  
    return render(request, 'test/students.html', {
        "has_students": has_students, 
        "student_list": all_students if has_students else None,
        "form": form
    })
    
@login_required
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

@login_required
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
    
@login_required
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
        
@login_required
def download_violation_files(request):
    # Get the StudentViolation object
    violation_id = request.GET.get('violation_id')
    violation = get_object_or_404(StudentViolation, id=violation_id)
    student_id = violation.student.id
    print(f"Student ID={violation.student.id}" )
    violation_files = violation.violation_files.all()
    if violation_files: 
        # Create an in-memory ZIP file
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            # Get all related files
            # Add each file to the zip
            for violation_file in violation_files:
                file_path = violation_file.file.path  # Full file path on disk
                file_name = os.path.basename(file_path)  # Extract the filename
                zip_file.write(file_path, file_name)  # Add file to the ZIP

        # Set the pointer of the BytesIO object back to the start
        zip_buffer.seek(0)

        # Create an HTTP response with the appropriate headers
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename=violation_files_{violation.id}.zip'

        return response
    else: 
        messages.add_message(request, messages.ERROR, "No files attached to record.")
        return HttpResponseRedirect(f'/view-student/?student_id={student_id}')

def view_violations(request):
    major = Violation.objects.all().filter(violation_class__exact="Major")
    minor = Violation.objects.all().filter(violation_class__exact="Minor")
    form = ViolationForm()
    return render(request, "test/violations.html",{
        "major": major,
        "minor": minor,
        "form": form
    })
    
def add_violation(request):
    if(request.method == "POST"):
        form = ViolationForm(request.POST)
        if form.errors:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, "%s: %s" %(error, form.errors[error]))
            return HttpResponseRedirect('/violations/')
        if form.is_valid(): 
            record = form.save(commit=False)
            record.violation_class = request.POST.get('violation_class')  # Set the class from hidden input
            record.save()
            messages.add_message(request, messages.SUCCESS, "Added a violation record.")
            return HttpResponseRedirect('/violations/')
        
def toggle_pending(request):
    if(request.method == "POST"):
        violation_id = request.POST.get("violation_id")
        student_id = request.POST.get("student_id")
        try: 
            violation_record = StudentViolation.objects.get(id=violation_id)
        except StudentViolation.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Record does not exist.")
            return HttpResponseRedirect(f'/view-student/?student_id={student_id}')
        violation_record.status = not violation_record.status
        violation_record.save()
        messages.add_message(request, messages.SUCCESS, "Record updated.")
        return HttpResponseRedirect(f'/view-student/?student_id={student_id}')

@login_required
def edit_student_violation(request):
    if request.method == "POST":
        files = request.FILES.getlist('files')  # Get the uploaded files
        violation_id = request.POST.get("violation_id")
        student_id = request.POST.get("student_id")
        
        try:
            # Fetch the violation by ID
            violation = StudentViolation.objects.get(id=violation_id)
        except StudentViolation.DoesNotExist:
            messages.error(request, "Violation does not exist.")
            return HttpResponseRedirect(f'/view-student/?student_id={student_id}')
        
        # Process the form with the violation instance
        form = StudentViolationForm(request.POST, instance=violation)
        if form.is_valid():
            form.save(commit=False)  # Save the updated violation data
            current_time = datetime.now()
            form.time = current_time
            form.save()
            for file in files:
                StudentViolationFile.objects.create(student_violation=form, file=file)
            messages.success(request, "Violation updated successfully.")
        else:
            messages.error(request, "Failed to update violation.")
        
        return HttpResponseRedirect(f'/view-student/?student_id={student_id}')