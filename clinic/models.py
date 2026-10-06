from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Animal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="animals")
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.client.name})"


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="appointments"
    )
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="appointments"
    )
    scheduled_for = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    reason = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCHEDULED
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_for"]

    def __str__(self):
        return f"{self.animal.name} at {self.scheduled_for:%Y-%m-%d %H:%M}"

    def clean(self):
        errors = {}

        if self.animal_id and self.client_id and self.animal.client_id != self.client_id:
            errors["animal"] = "The selected animal does not belong to this client."

        if self.duration_minutes <= 0:
            errors["duration_minutes"] = "Duration must be greater than zero."

        if (
            self.status == self.Status.SCHEDULED
            and self.scheduled_for
            and self.scheduled_for < timezone.now()
        ):
            errors["scheduled_for"] = "A new appointment cannot be in the past."

        if self.status == self.Status.SCHEDULED and self.scheduled_for and self.animal_id:
            appointment_end = self.scheduled_for + timedelta(minutes=self.duration_minutes)
            conflicts = Appointment.objects.filter(
                animal_id=self.animal_id,
                status=self.Status.SCHEDULED,
                scheduled_for__lt=appointment_end,
            ).exclude(pk=self.pk)
            for conflict in conflicts:
                conflict_end = conflict.scheduled_for + timedelta(
                    minutes=conflict.duration_minutes
                )
                if conflict_end > self.scheduled_for:
                    errors["scheduled_for"] = (
                        "This animal already has an appointment at that time."
                    )
                    break

        if errors:
            raise ValidationError(errors)