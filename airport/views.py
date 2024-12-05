from django.db.models import Count, F
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flight, Route, Airport, Crew, Ticket, Order, Airplane, AirplaneType, User
from .serializers import RouteListSerializer, RouteRetrieveSerializer, RouteSerializer, AirportSerializer, \
    CrewSerializer, TicketSerializer, \
    OrderRetrieveSerializer, OrderListSerializer, AirplaneSerializer, AirplaneTypeSerializer, FlightListSerializer, \
    FlightRetrieveSerializer, \
    FlightSerializer, OrderSerializer, TicketListSerializer, UserRegistrationSerializer


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
        queryset = (Flight.objects.all().select_related("airplane", "route__source", "route__destination").
                    prefetch_related("tickets"))
        code = self.request.query_params.get("code")
        if code:
            queryset = queryset.filter(code__icontains=code)
        if self.action == "retrieve":
            queryset = ((queryset.annotate(taken_seats=Count("tickets"))).
                        annotate(available_seats=F("airplane__rows") * F("airplane__seats_in_row") - F("taken_seats")))
        return queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer

    def get_queryset(self):
        return self.queryset.select_related("source", "destination")


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

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.select_related("order, order__user",).filter(order__user=self.request.user)
        return self.queryset.select_related()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderSerializer

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user).select_related()
        return self.queryset


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Correctly placed here

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
