import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """ Django Command to pause execution till the database is available"""
        self.stdout.write("Waiting for Database.....")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 sec...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
