from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from rest_framework import viewsets, status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flight, Route, Airport, Crew, Ticket, Order, Airplane, AirplaneType
from .serializers import RouteListSerializer, RouteRetrieveSerializer, RouteSerializer, AirportSerializer, \
    CrewSerializer, \
    OrderRetrieveSerializer, OrderListSerializer, AirplaneSerializer, AirplaneTypeSerializer, FlightListSerializer, \
    FlightRetrieveSerializer, \
    FlightSerializer, OrderSerializer, TicketListSerializer


@extend_schema_view(
    list=extend_schema(
        description="List all flights",
        request=RouteListSerializer,
        responses={
            200: RouteListSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    retrieve=extend_schema(
        description="Retrieve a flight",
        request=RouteRetrieveSerializer,
        responses={
            200: RouteRetrieveSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    create=extend_schema(
        description="Create a new route.",
        request=RouteSerializer,
        responses={
            201: RouteSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    update=extend_schema(
        description="Update an existing route.",
        request=RouteSerializer,
        responses={
            200: RouteSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    partial_update=extend_schema(
        description="Partially update an existing route.",
        request=RouteSerializer,
        responses={
            200: RouteSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    destroy=extend_schema(
        description="Delete an existing route.",
        responses={
            204: OpenApiResponse(description="No content"),
            400: OpenApiResponse(description="Bad request")
        }
    ),
)
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


class TicketList(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketListSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            self.queryset = self.queryset.filter(order__user=self.request.user)
        self.queryset = self.queryset.select_related("order", "flight", "order__user")
        return self.queryset


@extend_schema_view(
    list=extend_schema(
        responses={
            200: OrderListSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    retrieve=extend_schema(
        responses={
            200: OrderRetrieveSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    create=extend_schema(
        description="Create a new order.",
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    update=extend_schema(
        description="Update an existing order.",
        request=OrderSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    partial_update=extend_schema(
        description="Partially update an existing order.",
        request=RouteSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Bad request")
        }
    ),
    destroy=extend_schema(
        description="Delete an existing order.",
        responses={
            204: OpenApiResponse(description="No content"),
            400: OpenApiResponse(description="Bad request")
        }
    ),
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if not self.request.user.is_staff:
            self.queryset = self.queryset.filter(user=self.request.user)
        self.queryset = self.queryset.select_related("user").prefetch_related("tickets__flight")
        return self.queryset


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer



@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of flights. Optionnaly filtering by flight code",
        request=FlightListSerializer,
        parameters=[
            OpenApiParameter(
                name="code",
                type=str,
                required=False,
                description="Find the flight by code"
            )
        ],
        responses={
            200: FlightListSerializer,
            400: OpenApiResponse(
                description="Bad request"
            )

        }
    ),
    retrieve=extend_schema(
        description="Retrieve a flight",
        request=FlightRetrieveSerializer,
        responses={
            200: FlightRetrieveSerializer,
            400: OpenApiResponse(
                description="Bad request"
            )
        }
    ),
    update=extend_schema(
        request=FlightSerializer,
        description="Update a flight",
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(
                description="Bad request"
            )
        }
    ),
    partial_update=extend_schema(
        request=FlightSerializer,
        description="Partially update flight",
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(
                description="Bad request"
            )
        }
    ),
    destroy=extend_schema(
        description="Deleting the flight",
        responses={
            20: OpenApiResponse(description="Delete the flight"),
            400: OpenApiResponse(description="Bad request"),
        }
    )

)
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
        queryset = (Flight.objects.all()
                    .select_related("airplane", "route__source", "route__destination")
                    .prefetch_related("tickets"))
        code = self.request.query_params.get("code")
        if code:
            queryset = queryset.filter(code__icontains=code)
        if self.action == "retrieve":
            queryset = (
                queryset
                .annotate(taken_seats=Count("tickets"))
                .annotate(available_seats=F("airplane__rows") * F("airplane__seats_in_row") - F("taken_seats"))
            )
        return queryset
