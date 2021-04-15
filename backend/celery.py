from celery import Celery
import os
from django.conf import settings
import django
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("zerodha")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'csv-parsing': {
        'task': 'core.tasks.process_csv',
        'schedule': crontab(minute = '*/1', day_of_week = '1-5'),
    },
}
app.conf.timezone = 'Asia/Kolkata'