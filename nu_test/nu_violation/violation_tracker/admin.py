from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Student)
admin.site.register(Violation)
admin.site.register(StudentViolation)
admin.site.register(StudentViolationFile)
