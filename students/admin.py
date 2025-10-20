from django.contrib import admin
from .models import StudentProfile, Attendance

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'full_name', 'phone', 'email', 'token')
    search_fields = ('full_name', 'roll_number', 'phone', 'email')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'time', 'present', 'marked_via')
    list_filter = ('date', 'present')
    search_fields = ('student__full_name','student__roll_number')
