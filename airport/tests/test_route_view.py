from datetime import timezone, datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from airport.models import Route, Airport
from airport.serializers import RouteListSerializer, RouteRetrieveSerializer


class RouteViewIsNotAuthenticatedTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_connection(self):

        url = reverse("airport:route-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)  # Unauthorized access


class RouteViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@gmail.com", "123456admin"
        )
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @classmethod
    def setUpTestData(cls):

        # Create airports and routes
        cls.airport1 = Airport.objects.create(
            name="Airport A", closest_big_city="City A"
        )
        cls.airport2 = Airport.objects.create(
            name="Airport B", closest_big_city="City B"
        )
        cls.airport3 = Airport.objects.create(
            name="Airport C", closest_big_city="City C"
        )

        cls.route_1 = Route.objects.create(
            source=cls.airport1,
            destination=cls.airport2,
            distance=200,
        )
        cls.route_2 = Route.objects.create(
            source=cls.airport2,
            destination=cls.airport3,
            distance=300,
        )

    def test_list_routes(self):
        """
        Test the list endpoint returns a valid list of routes.
        """
        url = reverse("airport:route-list")
        res = self.client.get(url)
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_route(self):

        url = reverse("airport:route-detail", kwargs={"pk": self.route_1.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = RouteRetrieveSerializer(self.route_1)
        self.assertEqual(res.data, serializer.data)

    def test_create_route(self):

        payload = {
            "source": self.airport1.id,
            "destination": self.airport3.id,
            "distance": 400,
        }
        url = reverse("airport:route-list")
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["distance"], 400)
