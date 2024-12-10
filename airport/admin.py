from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Flight, Route, Airport, Crew, Ticket, Order, Airplane, AirplaneType


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    pass


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    pass


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    pass


# Register your models here.
class UserAdminR(UserAdmin):
    pass
