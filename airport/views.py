from django.db.models import Count, F
from rest_framework import viewsets
from .models import Flight, Route, Airport, Crew, Ticket, Order, Airplane, AirplaneType
from .serializers import RouteListSerializer, RouteRetrieveSerializer, RouteSerializer, AirportSerializer, \
    CrewSerializer, TicketSerializer, \
    OrderRetrieveSerializer, OrderListSerializer, AirplaneSerializer, AirplaneTypeSerializer, FlightListSerializer, \
    FlightRetrieveSerializer, \
    FlightSerializer, OrderSerializer, TicketListSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightRetrieveSerializer
        else:
            return FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.all()
        code = self.request.query_params.get("code")
        if code:
            queryset = queryset.filter(code__icontains=code)
        if self.action == "retrieve":
            queryset = ((queryset.select_related("route").select_related("airplane").
                         prefetch_related("tickets").annotate(taken_seats=Count("tickets"))).
                        annotate(available_seats=F("airplane__rows") * F("airplane__seats_in_row") - F("taken_seats")))
        elif self.action == "list":
            queryset = (queryset.select_related("route").select_related("airplane"))
        return queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
