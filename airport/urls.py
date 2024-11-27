from django.urls import path
from rest_framework import routers

from airport.views import FlightViewSet, AirportViewSet, OrderViewSet, RouteViewSet, CrewViewSet, AirplaneViewSet, \
    AirplaneTypeViewSet, TicketViewSet

urlpatterns = [
]

router = routers.DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'airports', AirportViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'crews', CrewViewSet)
router.register(r'airplanes', AirplaneViewSet)
router.register(r'airplane_types', AirplaneTypeViewSet)
router.register(r'tickets', TicketViewSet)
urlpatterns += router.urls

app_name = 'airport'
