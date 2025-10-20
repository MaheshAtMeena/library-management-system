from django.apps import AppConfig

class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'

    def ready(self):
        # import signals
        try:
            import students.signals
        except Exception:
            pass
