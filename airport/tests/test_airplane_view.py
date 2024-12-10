from datetime import timezone, datetime
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import Airplane, AirplaneType
from airport.serializers import AirplaneSerializer


class AirplaneViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user1@example.com", password="securepassword"
        )
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @classmethod
    def setUpTestData(cls):
        cls.airplane_type_1 = AirplaneType.objects.create(name="Boeing 747")
        cls.airplane_type_2 = AirplaneType.objects.create(name="Airbus A320")

        cls.airplane_1 = Airplane.objects.create(
            name="Airplane 1",
            rows=20,
            seats_in_row=6,
            airplane_type=cls.airplane_type_1,
        )
        cls.airplane_2 = Airplane.objects.create(
            name="Airplane 2",
            rows=25,
            seats_in_row=8,
            airplane_type=cls.airplane_type_2,
        )

        cls.airplane_list_url = reverse("airport:airplane-list")
        cls.airplane_detail_url = lambda pk: reverse(
            "airport:airplane-detail", args=[pk]
        )

    def test_get_airplane_list(self):
        response = self.client.get(self.airplane_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_single_airplane(self):
        response = self.client.get(self.airplane_detail_url(self.airplane_1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Airplane 1")
        self.assertEqual(response.data["rows"], 20)

    def test_create_airplane(self):
        payload = {
            "name": "Airplane 3",
            "rows": 30,
            "seats_in_row": 10,
            "airplane_type": self.airplane_type_1.id,
        }
        response = self.client.post(self.airplane_list_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Airplane 3")
        self.assertEqual(response.data["rows"], 30)
