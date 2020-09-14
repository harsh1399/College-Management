from django.apps import AppConfig


class CollegeInfoConfig(AppConfig):
    name = 'college_info'

    def ready(self):
        import college_info.signals