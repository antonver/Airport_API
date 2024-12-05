import string

from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from airport.models import (
    Flight, Route, Airport, Crew, Ticket, Order,
    Airplane, AirplaneType
)


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating the database with sample data...")




        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
