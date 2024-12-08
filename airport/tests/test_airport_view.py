from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import Airport


class AirportViewSetTests(APITestCase):
    def setUp(self):

        self.airport_1_data = {"name": "JFK", "closest_big_city": "New York"}
        self.airport_2_data = {"name": "LAX", "closest_big_city": "Los Angeles"}

        self.airport_1 = Airport.objects.create(**self.airport_1_data)
        self.airport_2 = Airport.objects.create(**self.airport_2_data)
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@gmail.com", "123456admin")
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        self.url_list = reverse("airport:airport-list")
        self.url_detail = reverse("airport:airport-detail", args=[self.airport_1.id])


    def test_get_airport_list(self):

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data["results"]), 2)  # There should be two airports in the DB

    def test_create_airport(self):

        new_airport_data = {"name": "ORD", "closest_big_city": "Chicago"}
        response = self.client.post(self.url_list, new_airport_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "ORD")
        self.assertEqual(response.data["closest_big_city"], "Chicago")

    def test_get_airport_detail(self):

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "JFK")
        self.assertEqual(response.data["closest_big_city"], "New York")