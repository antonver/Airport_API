from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from datetime import datetime, timezone

from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import Order


class OrderViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create_user(
            email="user1@example.com", password="securepassword"
        )
        cls.user_2 = get_user_model().objects.create_user(
            email="user2@example.com", password="securepassword", is_staff=True
        )
        cls.order_1 = Order.objects.create(
            user=cls.user_1, created_at=datetime.now(tz=timezone.utc)
        )
        cls.order_2 = Order.objects.create(
            user=cls.user_2, created_at=datetime.now(tz=timezone.utc)
        )

        cls.order_list_url = reverse("airport:order-list")
        cls.order_detail_user_1 = reverse("airport:order-detail", args=[cls.order_1.id])
        cls.order_detail_user_2 = reverse("airport:order-detail", args=[cls.order_2.id])

    def test_list_orders_unauthenticated(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_orders_authenticated(self):
        self.client = APIClient()
        token = RefreshToken.for_user(self.user_1).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_staff_can_access_all_orders(self):
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
