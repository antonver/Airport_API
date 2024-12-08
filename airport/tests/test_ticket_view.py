from datetime import datetime, timedelta, timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import Airport, Route, AirplaneType, Airplane, Flight, Ticket, Order


class TicketViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users for testing
        cls.user = get_user_model().objects.create_user(
            email="user1@example.com", password="securepassword"
        )
        cls.user2 = get_user_model().objects.create_user(
            email="user22@example.com", password="securepassword", is_staff=True
        )

        # Create airports
        cls.airport1 = Airport.objects.create(name="JFK", closest_big_city="New York")
        cls.airport2 = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")

        # Create a route
        cls.route = Route.objects.create(
            source=cls.airport1,
            destination=cls.airport2,
            distance=4000,
        )

        # Create airplane type
        cls.airplane_type = AirplaneType.objects.create(name="Boeing 747")

        # Create airplane
        cls.airplane = Airplane.objects.create(
            name="Airplane 1",
            rows=20,
            seats_in_row=6,
            airplane_type=cls.airplane_type,
        )

        # Create flight
        cls.flight = Flight.objects.create(
            code="FL1234",
            route=cls.route,
            airplane=cls.airplane,
            departure_time=datetime.now(tz=timezone.utc) + timedelta(days=1),
            arrival_time=datetime.now(tz=timezone.utc) + timedelta(days=1, hours=5),
        )

        # Create orders
        cls.order = Order.objects.create(
            user=cls.user,
            created_at=datetime.now(tz=timezone.utc)
        )

        cls.order2 = Order.objects.create(
            user=cls.user2,
            created_at=datetime.now(tz=timezone.utc)
        )

        # Create tickets
        cls.ticket1 = Ticket.objects.create(
            row=10,
            seat="10A",
            flight=cls.flight,
            order=cls.order,
        )
        cls.ticket2 = Ticket.objects.create(
            row=12,
            seat="12B",
            flight=cls.flight,
            order=cls.order,
        )
        cls.ticket3 = Ticket.objects.create(
            row=11,
            seat="11A",
            flight=cls.flight,
            order=cls.order2,
        )
        cls.ticket4 = Ticket.objects.create(
            row=11,
            seat="11B",
            flight=cls.flight,
            order=cls.order2,
        )

    def setUp(self):

        token = RefreshToken.for_user(self.user).access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_ticket_list(self):
        url = reverse("airport:ticket-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_ticket_creation(self):

        url = reverse("airport:ticket-list")
        payload = {
            "row": 14,
            "seat": "C",
            "flight": self.flight.id,
            "order": self.order.id,
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 405)
