from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # ✅ Unique username validation
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Choose another.")
        return username


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['roll_number', 'full_name', 'dob', 'father_name', 'phone', 'email']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'roll_number': 'Table Seat Number',  # ✅ Label changed here
        }
