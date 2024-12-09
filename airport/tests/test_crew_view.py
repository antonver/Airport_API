from datetime import timezone, datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import Crew


class CrewViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@gmail.com", "123456admin"
        )
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @classmethod
    def setUpTestData(cls):
        cls.crew_1 = Crew.objects.create(first_name="John", last_name="Doe")
        cls.crew_2 = Crew.objects.create(first_name="Jane", last_name="Smith")
        cls.url_list = reverse("airport:crew-list")
        cls.url_detail_1 = reverse("airport:crew-detail", args=[cls.crew_1.id])
        cls.url_detail_2 = reverse("airport:crew-detail", args=[cls.crew_2.id])

    def test_get_crew_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_crew_member(self):
        payload = {"first_name": "Alice", "last_name": "Wonderland"}
        response = self.client.post(self.url_list, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], "Alice")
        self.assertEqual(response.data["last_name"], "Wonderland")

    def test_get_crew_detail(self):
        response = self.client.get(self.url_detail_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_update_crew_member(self):
        payload = {"first_name": "Johnny", "last_name": "Doe"}
        response = self.client.put(self.url_detail_1, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Johnny")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_partial_update_crew_member(self):
        payload = {"last_name": "Doe-Smith"}
        response = self.client.patch(self.url_detail_2, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["last_name"], "Doe-Smith")
        self.assertEqual(response.data["first_name"], "Jane")

    def test_delete_crew_member(self):
        response = self.client.delete(self.url_detail_1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.url_detail_1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
