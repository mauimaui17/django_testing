from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.homepage, name="homepage"),
    path("", views.homepage, name="homepage"),
    path("base/", views.base, name="base"),
    path("students/", views.students, name="students"),
    path("add-student/", views.add_student, name="add-student"),
    path("view-student/", views.view_student, name="view-student"),
    
]