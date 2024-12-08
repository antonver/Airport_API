from datetime import timezone, datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import Airport, Route, AirplaneType, Airplane, Flight
from airport.serializers import FlightListSerializer, FlightSerializer, FlightRetrieveSerializer


class FlightViewIsNotAuthenticatedTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_connection(self):
        url = reverse("airport:flight-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)




class FlightViewIsAuthenticatedTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@gmail.com", "123456admin")
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @classmethod
    def setUpTestData(cls):

        cls.airport1 = Airport.objects.create(name="JFK", closest_big_city="New York")
        cls.airport2 = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")

        cls.route = Route.objects.create(
            source=cls.airport1,
            destination=cls.airport2,
            distance=4000,
        )

        cls.airplane_type = AirplaneType.objects.create(name="Boeing 747")

        cls.airplane = Airplane.objects.create(
            name="Airplane 1",
            rows=20,
            seats_in_row=6,
            airplane_type=cls.airplane_type,
        )

        # Create sample flights
        cls.flight1 = Flight.objects.create(
            code="FL1234",
            route=cls.route,
            airplane=cls.airplane,
            departure_time=datetime.now() + timedelta(days=1),
            arrival_time=datetime.now() + timedelta(days=1, hours=5),
        )

        cls.flight2 = Flight.objects.create(
            code="FL5678",
            route=cls.route,
            airplane=cls.airplane,
            departure_time=datetime.now() + timedelta(days=2),
            arrival_time=datetime.now() + timedelta(days=2, hours=4),
        )

    def test_connection(self):
        url = reverse("airport:flight-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_flight_list(self):
        url = reverse("airport:flight-list")
        res = self.client.get(url)
        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_flight_by_code(self):
        url = reverse("airport:flight-list")
        res = self.client.get(url, {"code": "FL1234"})
        flight = Flight.objects.filter(code__iexact="Fl1234")
        serializer = FlightListSerializer(flight, many=True)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_flight_by_id(self):
        url = reverse("airport:flight-detail", args=[1,])
        res = self.client.get(url)
        flight = Flight.objects.get(id=1)
        serializer = FlightRetrieveSerializer(flight)
        res.data.pop("available_seats")
        res.data.pop("taken_seats")
        self.assertEqual(res.data, serializer.data)

    def test_create_correct_date_flight(self):
        payload = {
            "code":"FL5699",
            "route":1,
            "airplane":1,
            "departure_time": "2024-11-25T16:20:15",
            "arrival_time": "2024-12-25T16:20:15"
        }
        url = reverse("airport:flight-list")
        res = self.client.post(url, payload)
        flight = Flight.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            if key == "route":
                self.assertEqual(payload[key], flight.route.id)
            elif key == "airplane":
                self.assertEqual(payload[key], flight.airplane.id)
            elif key in ["departure_time", "arrival_time"]:  # Handle datetime comparison with tzinfo
                expected_datetime = datetime.fromisoformat(payload[key]).replace(tzinfo=timezone.utc)
                self.assertEqual(expected_datetime, getattr(flight, key))
            else:
                self.assertEqual(payload[key], getattr(flight, key))

    def test_create_incorrect_date_flight(self):
        payload = {
            "code":"FL5699",
            "route":1,
            "airplane":1,
            "departure_time": "2024-11-25T16:20:15",
            "arrival_time": "2024-10-25T16:20:15"
        }
        url = reverse("airport:flight-list")
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
