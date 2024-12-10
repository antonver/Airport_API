import random
import string
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Crew,
    Ticket,
    Order,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs):
        # Generate sample data
        self.stdout.write("Populating database...")

        # Create Airports
        airport_names = [
            "John F Kennedy",
            "LAX",
            "Heathrow",
            "Narita",
            "Charles de Gaulle",
        ]
        big_cities = ["New York", "Los Angeles", "London", "Tokyo", "Paris"]
        airports = []
        for name, city in zip(airport_names, big_cities):
            airport = Airport.objects.create(name=name, closest_big_city=city)
            airports.append(airport)
        self.stdout.write(f"Created {len(airports)} airports.")

        # Create Routes
        routes = []
        for i in range(len(airports) - 1):
            route = Route.objects.create(
                source=airports[i],
                destination=airports[i + 1],
                distance=random.randint(100, 10000),
            )
            routes.append(route)
        self.stdout.write(f"Created {len(routes)} routes.")

        # Create Airplane Types
        airplane_types = []
        for i in range(3):
            airplane_type = AirplaneType.objects.create(name=f"Type-{i + 1}")
            airplane_types.append(airplane_type)
        self.stdout.write(f"Created {len(airplane_types)} airplane types.")

        # Create Airplanes
        airplanes = []
        for i in range(5):
            airplane = Airplane.objects.create(
                name=f"Airplane-{i + 1}",
                rows=random.randint(10, 30),
                seats_in_row=random.randint(4, 10),
                airplane_type=random.choice(airplane_types),
            )
            airplanes.append(airplane)
        self.stdout.write(f"Created {len(airplanes)} airplanes.")

        # Create Flights
        flights = []
        for i in range(10):
            flight = Flight.objects.create(
                code="".join(
                    random.choices(string.ascii_uppercase + string.digits, k=6)
                ),
                route=random.choice(routes),
                airplane=random.choice(airplanes),
                departure_time=datetime.now() + timedelta(days=random.randint(1, 30)),
                arrival_time=datetime.now() + timedelta(days=random.randint(31, 60)),
            )
            flights.append(flight)
        self.stdout.write(f"Created {len(flights)} flights.")

        # Create Crews
        crew_names = ["John", "Jane", "Paul", "Anna", "Mike", "Sara", "Tom", "Eva"]
        crews = []
        for i in range(5):
            crew = Crew.objects.create(
                first_name=random.choice(crew_names),
                last_name=random.choice(crew_names),
            )
            crews.append(crew)
        self.stdout.write(f"Created {len(crews)} crew members.")

        # Create Users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                password="password123", email=f"user{i + 1}@example.com"
            )
            users.append(user)
        self.stdout.write(f"Created {len(users)} users.")

        # Create Orders
        orders = []
        for i in range(10):
            order = Order.objects.create(
                created_at=datetime.now(), user=random.choice(users)
            )
            orders.append(order)
        self.stdout.write(f"Created {len(orders)} orders.")

        # Create Tickets
        tickets = []
        for i in range(20):
            flight = random.choice(flights)
            row = random.randint(1, flight.airplane.rows)
            seat = f"{row}{random.choice(string.ascii_uppercase[:flight.airplane.seats_in_row])}"
            ticket = Ticket.objects.create(
                row=row, seat=seat, flight=flight, order=random.choice(orders)
            )
            tickets.append(ticket)
        self.stdout.write(f"Created {len(tickets)} tickets.")

        self.stdout.write("Database population complete!")
