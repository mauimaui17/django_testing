from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.homepage, name="homepage"),
    path("", views.homepage, name="homepage"),
    
    path("base/", views.base, name="base"),
    path("students/", views.students, name="students"),
    
]