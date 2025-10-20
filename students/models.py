import uuid, datetime
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    dob = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"


class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(auto_now_add=True)
    present = models.BooleanField(default=True)
    marked_via = models.CharField(max_length=50, default='web')

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {'Present' if self.present else 'Absent'}"
