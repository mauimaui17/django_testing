from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.homepage, name="homepage"),
    path("handbook/", views.handbook, name="handbook"),
    path("", views.homepage, name="homepage"),
    path("base/", views.base, name="base"),
    path("students/", views.students, name="students"),
    path("add-student/", views.add_student, name="add-student"),
    path("view-student/", views.view_student, name="view-student"),
    path("add-student-violation/", views.add_student_violation, name="add-student-violation"),
    path("get-files/", views.download_violation_files, name="get-files"),
    path("violations/", views.view_violations, name="violations"),
    path("add-violation/", views.add_violation, name="add-violation"),
    path("toggle-pending/", views.toggle_pending, name="toggle-pending"),
    path("edit-student-violation/", views.edit_student_violation, name="edit-student-violation"),
    
]