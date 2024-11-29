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

        # Create Airplane Types
        airplane_types = [
            AirplaneType.objects.create(name=f"Type-{i}") for i in range(1, 4)
        ]

        # Create Airplanes
        airplanes = [
            Airplane.objects.create(
                name=f"Airplane-{i}",
                rows=random.randint(20, 40),
                seats_in_row=random.randint(4, 8),
                airplane_type=random.choice(airplane_types)
            )
            for i in range(5)
        ]

        # Create Airports
        airports = [
            Airport.objects.create(
                name=f"Airport-{i}",
                closest_big_city=f"City-{i}"
            )
            for i in range(10)
        ]

        # Create Routes
        routes = [
            Route.objects.create(
                source=random.choice(airports),
                destination=random.choice([a for a in airports if a != airports[i]]),
                distance=random.randint(100, 5000)
            )
            for i in range(len(airports) - 1)
        ]

        # Create Flights
        flights = []
        for route in routes:
            for i in range(random.randint(1, 3)):  # Multiple flights per route
                departure_time = datetime.now() + timedelta(days=random.randint(1, 30))
                flights.append(Flight.objects.create(
                    route=route,
                    airplane=random.choice(airplanes),
                    departure_time=departure_time,
                    arrival_time=departure_time + timedelta(hours=random.randint(2, 12))
                ))

        # Create Users
        User = get_user_model()
        users = [User.objects.create_user(username=f"user{i}", password="password") for i in range(5)]

        # Create Orders
        orders = [
            Order.objects.create(
                created_at=datetime.now() - timedelta(days=random.randint(1, 10)),
                user=random.choice(users)
            )
            for i in range(10)
        ]

        # Create Tickets
        for order in orders:
            flight = random.choice(flights)
            airplane = flight.airplane
            for _ in range(random.randint(1, 3)):
                row = random.randint(1, airplane.rows)

                Ticket.objects.create(
                    row=row,
                    seat=f"{row}{string.ascii_uppercase[random.randint(0, airplane.seats_in_row-1)]}",
                    flight=flight,
                    order=order
                )

        # Create Crew
        for _ in range(15):
            Crew.objects.create(
                first_name=f"First-{random.randint(1, 100)}",
                last_name=f"Last-{random.randint(1, 100)}"
            )

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
