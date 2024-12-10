import string

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from airport_api import settings


# Create your models here.
class Flight(models.Model):
    code = models.CharField(max_length=7, null=True, blank=True)
    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(
        "Airplane", on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return self.code


class Route(models.Model):
    source = models.ForeignKey(
        "Airport", on_delete=models.CASCADE, related_name="routes_from"
    )
    destination = models.ForeignKey(
        "Airport", on_delete=models.CASCADE, related_name="routes_to"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"Distance: {self.id};"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"Closest big city: {self.closest_big_city}; Airport: {self.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.CharField(max_length=5)
    flight = models.ForeignKey(
        "Flight", on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("seat", "flight", "row")

    @staticmethod
    def validate_tickets(seat, row, seats_in_row, rows, error_to_rise):
        possible_seats_in_row = [
            list(string.ascii_uppercase)[i] for i in range(seats_in_row)
        ]
        if (
            seat[-1] not in possible_seats_in_row
            or row != int(seat[:-1])
            or row < 0
            or row > rows
        ):
            raise error_to_rise(
                {"seat": f"in the  plane {seats_in_row} seats in a row and {rows} rows"}
            )

    def clean(self):
        self.validate_tickets(
            self.seat,
            self.row,
            self.flight.airplane.seats_in_row,
            self.flight.airplane.rows,
            ValidationError,
        )
        super().clean()

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Flight code: {self.flight.code}; Seat:{self.seat}; Row:{self.row};"


class Order(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        formatted_date = self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )  # Format the date-time
        return f"Created at {formatted_date}"


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType", on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self):
        return f"{self.name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
