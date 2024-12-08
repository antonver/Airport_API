from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer


class AirplaneTypeViewSetTests(APITestCase):
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
        cls.airplane_type_list_url = reverse("airport:airplanetype-list")
        cls.airplane_type_detail_url = lambda pk: reverse("airport:airplanetype-detail", args=[pk])

    def test_get_airplane_type_list(self):
        response = self.client.get(self.airplane_type_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_single_airplane_type(self):
        response = self.client.get(self.airplane_type_detail_url(self.airplane_type_1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Boeing 747")

    def test_create_airplane_type(self):
        payload = {"name": "Concorde"}
        response = self.client.post(self.airplane_type_list_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Concorde")
