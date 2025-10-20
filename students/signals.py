from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        # create a blank StudentProfile (admin can edit later)
        StudentProfile.objects.create(user=instance, full_name=instance.get_full_name() or instance.username, roll_number=f'R{instance.id:04d}')
