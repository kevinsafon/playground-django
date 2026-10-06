from django.contrib import admin

from clinic.models import Animal, Appointment, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "breed", "client")
    list_filter = ("species",)
    search_fields = ("name", "client__name")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("scheduled_for", "animal", "client", "status", "reason")
    list_filter = ("status", "scheduled_for")
    search_fields = ("animal__name", "client__name", "reason")