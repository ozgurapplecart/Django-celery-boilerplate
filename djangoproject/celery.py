import os
from celery import Celery
from celery.utils.log import get_task_logger
from mekan_com_fetcher.mekan_com_fetcher import MekanComFetcher

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

logger = get_task_logger(__name__)


@app.task(bind=True)
def debug_task(self):
    logger.info("The sample task just ran.")

@app.task(bind=True)
def fetch_mekan_com(self):
    s = MekanComFetcher()
    s.setup()
    s.run()
    s.prepare_results()