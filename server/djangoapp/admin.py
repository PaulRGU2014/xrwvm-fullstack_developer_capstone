from django.contrib import admin
from .models import CarMake, CarModel

# Registering models with their respective admins

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
	list_display = ("name", "created_at")
	search_fields = ("name",)
	ordering = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
	list_display = ("name", "car_make", "type", "year")
	list_filter = ("type", "year", "car_make")
	search_fields = ("name", "car_make__name")
	ordering = ("car_make__name", "name")