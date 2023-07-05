from datetime import timedelta, time, datetime
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
from app.mekan_com_fetcher.mekan_com_fetcher import MekanComFetcher


today = timezone.now()
tomorrow = today + timedelta(1)
today_start = make_aware(datetime.combine(today, time()))
today_end = make_aware(datetime.combine(tomorrow, time()))


class Command(BaseCommand):
    help = "Send Today's Orders Report to Admins"

    def handle(self, *args, **options):
        print('dsds')