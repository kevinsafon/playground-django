from django import forms

from clinic.models import Animal, Appointment, Client


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget_class = (
                "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            )
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} {widget_class}".strip()


class ClientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone", "address", "notes"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class AnimalForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["name", "species", "breed", "date_of_birth", "notes"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class AppointmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "animal",
            "scheduled_for",
            "duration_minutes",
            "reason",
            "status",
            "notes",
        ]
        widgets = {
            "scheduled_for": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, client=None, **kwargs):
        super().__init__(*args, **kwargs)
        client = client or getattr(self.instance, "client", None)
        if client is None:
            self.fields["animal"].queryset = Animal.objects.none()
        else:
            self.fields["animal"].queryset = Animal.objects.filter(client=client)