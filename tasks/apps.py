from django.apps import AppConfig


class TskMngrConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        import tasks.signals
