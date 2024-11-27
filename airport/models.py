from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from airpot_api import settings


# Create your models here.
class Flight(models.Model):
    code = models.CharField(max_length=7, null=True, blank=True)
    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey("Airplane", on_delete=models.CASCADE, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()


class Route(models.Model):
    source = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="routes_from")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="routes_to")
    distance = models.IntegerField()


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")


class Order(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE, related_name="airplanes")


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)


class User(AbstractUser):
    def __str__(self):
        return self.username
