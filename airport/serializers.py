from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Flight, Route, Airport, Crew, Ticket, Order, Airplane, AirplaneType


#airport serializers
class AirportRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["name", ]


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


#Rout serializers
class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ["source", "destination"]


class RouteRetrieveSerializer(serializers.ModelSerializer):
    airport_of_departure = serializers.CharField(read_only=True, source="source.name")
    airport_of_arrival = serializers.CharField(read_only=True, source="source.name")
    city_of_departure = serializers.CharField(read_only=True, source="source.closest_big_city")
    city_of_arrival = serializers.CharField(read_only=True, source="destination.closest_big_city")

    class Meta:
        model = Route
        fields = ["airport_of_departure", "airport_of_arrival", "city_of_departure", "city_of_arrival", "distance"]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"



#airplane serializers



#flight serializers
class FlightListSerializer(serializers.ModelSerializer):
    city_of_departure = serializers.CharField(read_only=True, source="route.source.closest_big_city")
    city_of_arrival = serializers.CharField(read_only=True, source="route.destination.closest_big_city")
    airplane = serializers.CharField(read_only=True, source="airplane.name")

    class Meta:
        model = Flight
        fields = ["code", "city_of_departure", "city_of_arrival", "departure_time", "arrival_time", "airplane"]


class FlightRetrieveSerializer(serializers.ModelSerializer):
    available_seats = serializers.IntegerField(read_only=True)
    taken_seats = serializers.IntegerField(read_only=True)
    route = RouteRetrieveSerializer(read_only=True)
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    departure_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Flight
        fields = ["code", "available_seats", "taken_seats", "departure_time", "arrival_time", "airplane", "route"]


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(many=False, queryset=Route.objects.all().select_related())
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    departure_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def validate(self, attrs):
        if attrs["departure_time"] >= attrs["arrival_time"]:
            raise serializers.ValidationError("The departure date must be before the arrival date")
        return attrs

    class Meta:
        model = Flight
        fields = "__all__"


#airport serializers
class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


#crew serializers
class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'


#ticket serializers

class TicketListSerializer(serializers.ModelSerializer):
    flight = serializers.CharField(source="flight.code")
    person_who_ordered = serializers.StringRelatedField(source="order.user")

    class Meta:
        model = Ticket
        fields = ["row", "seat", "flight", "person_who_ordered"]



#user serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', "is_staff"]


class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", ]


#order serializers
class OrderRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tickets = TicketListSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    user = UserOrderSerializer(read_only=True)
    tickets = TicketListSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(read_only=False, many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


#airplane serializers
class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = '__all__'



