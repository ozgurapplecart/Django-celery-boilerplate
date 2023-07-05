import os
from celery import Celery
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logger.info("The sample task just ran.")


@app.task(bind=True)
def send_email_report(self):
    call_command("email_report")
