from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from .models import StudentProfile, Attendance
from .forms import UserRegistrationForm, StudentProfileForm
from django.core.mail import send_mail
from django.conf import settings
import datetime

from django.shortcuts import render

# views.py
from django.shortcuts import render

def home(request):
    context = {
        'owner_name': 'Dr. Mahesh Meena',
        'owner_image': 'image/owner1.png',  # image ko static folder me rakhe
        'about_text': """
Dr. Mahesh Meena is a dedicated medical professional currently posted in Alawara village, Alwar district. 
He hails from the small village of Reni in Alwar and is deeply committed to serving rural communities. 

Education:
- MBBS from Sardar Patel Medical College

Current Work:
- Providing primary healthcare services in Alawara village
- Ensuring the well-being of local residents through medical care and awareness programs
"""
    }
    return render(request, 'students/home.html', context)



def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('mark_attendance')  # safe GET redirect
        else:
            error = "Invalid credentials"
    return render(request, 'students/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login_view')

def register(request):
    if request.method == 'POST':
        uform = UserRegistrationForm(request.POST)
        pform = StudentProfileForm(request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save(commit=False)
            user.set_password(uform.cleaned_data['password'])
            user.save()

            # Check if profile already exists for this user
            if not hasattr(user, 'studentprofile'):
                profile = pform.save(commit=False)
                profile.user = user
                profile.save()

            return redirect('login_view')
        else:
            print("User form errors:", uform.errors)
            print("Profile form errors:", pform.errors)
    else:
        uform = UserRegistrationForm()
        pform = StudentProfileForm()

    return render(request, 'students/register.html', {
        'uform': uform,
        'pform': pform,
    })


@login_required
def mark_attendance(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    today = datetime.date.today()
    attendance, created = Attendance.objects.get_or_create(student=student, date=today, defaults={'present': True, 'marked_via':'web'})
    if created:
        message = 'Attendance marked successfully!'
    else:
        message = 'Attendance already marked for today.'
    return render(request, 'students/attendance.html', {'message': message})

def mark_attendance_token(request, token):
    student = get_object_or_404(StudentProfile, token=token)
    today = datetime.date.today()
    attendance, created = Attendance.objects.get_or_create(student=student, date=today, defaults={'present': True, 'marked_via':'link'})
    if created:
        message = f'Attendance marked for {student.full_name}.'
    else:
        message = f'Attendance already marked today for {student.full_name}.'
    return render(request, 'students/attendance_token.html', {'message': message, 'student': student})

@staff_member_required
def admin_dashboard(request):
    today = datetime.date.today()
    all_students = StudentProfile.objects.all().order_by('roll_number')
    attendance_today = Attendance.objects.filter(date=today).select_related('student')
    
    # IDs of students marked present
    present_ids = set(a.student_id for a in attendance_today)
    
    # Prepare table records
    attendance_records = []
    for student in all_students:
        record = {
            'student_name': student.full_name,
            'roll_number': student.roll_number,
            'attendance_date': today,
            'status': 'Present' if student.id in present_ids else 'Absent'
        }
        attendance_records.append(record)
    
    total_students = all_students.count()
    present_today = len(present_ids)
    absent_today = total_students - present_today
    
    # Send absent emails only when explicitly requested (POST)
    if request.method == 'POST' and request.POST.get('send_absent_emails') == '1':
        for student in all_students:
            if student.id not in present_ids and student.email:
                send_mail(
                    subject=f'Absence Notice - {today}',
                    message=f'Dear {student.full_name},\n\nYou were marked absent in the library on {today}.\n\nRegards',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[student.email],
                    fail_silently=True,
                )

    context = {
        'attendance_records': attendance_records,
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'today': today,
    }
    
    return render(request, 'students/dashboard.html', context)
