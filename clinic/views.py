from datetime import date

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from clinic.forms import AnimalForm, AppointmentForm, ClientForm
from clinic.models import Animal, Appointment, Client


class DashboardView(TemplateView):
    template_name = "clinic/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        today = timezone.localdate()
        scheduled = Appointment.objects.filter(status=Appointment.Status.SCHEDULED)
        context.update(
            client_count=Client.objects.count(),
            animal_count=Animal.objects.count(),
            today_date=today,
            today_appointments=scheduled.filter(
                scheduled_for__date=today
            ).select_related("client", "animal"),
            upcoming_appointments=scheduled.filter(
                scheduled_for__gt=now
            ).exclude(scheduled_for__date=today).select_related("client", "animal")[:5],
        )
        return context


class ClientListView(ListView):
    model = Client
    template_name = "clinic/clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clinic/clients/client_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Client created successfully.")
        return response

    def get_success_url(self):
        return reverse("client-detail", args=[self.object.pk])


class ClientDetailView(DetailView):
    model = Client
    template_name = "clinic/clients/client_detail.html"
    context_object_name = "client_record"


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clinic/clients/client_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Client updated successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy("client-detail", kwargs={"pk": self.object.pk})


class AnimalCreateView(CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = "clinic/animals/animal_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_record"] = get_object_or_404(
            Client, pk=self.kwargs["client_pk"]
        )
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = get_object_or_404(Client, pk=self.kwargs["client_pk"])
        self.object.save()
        messages.success(self.request, "Animal added successfully.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("client-detail", args=[self.kwargs["client_pk"]])


class AnimalUpdateView(UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = "clinic/animals/animal_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(client_id=self.kwargs["client_pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_record"] = self.object.client
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Animal updated successfully.")
        return response

    def get_success_url(self):
        return reverse("client-detail", args=[self.kwargs["client_pk"]])


class AppointmentListView(ListView):
    model = Appointment
    template_name = "clinic/appointments/appointment_list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related("client", "animal")
        status = self.request.GET.get("status", "").strip()
        date_filter = self.request.GET.get("date", "").strip()
        valid_statuses = {choice.value for choice in Appointment.Status}
        if status in valid_statuses:
            queryset = queryset.filter(status=status)
        if date_filter:
            try:
                selected_date = date.fromisoformat(date_filter)
            except ValueError:
                selected_date = None
            if selected_date:
                queryset = queryset.filter(scheduled_for__date=selected_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_date"] = self.request.GET.get("date", "")
        context["status_choices"] = Appointment.Status.choices
        return context


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "clinic/appointments/appointment_form.html"

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["client_pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.get_client()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_record"] = self.get_client()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = self.get_client()
        self.object.save()
        messages.success(self.request, "Appointment booked successfully.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("appointment-detail", args=[self.object.pk])


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "clinic/appointments/appointment_detail.html"
    context_object_name = "appointment"

    def get_queryset(self):
        return super().get_queryset().select_related("client", "animal")


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "clinic/appointments/appointment_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(client_id=self.kwargs["client_pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.object.client
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_record"] = self.object.client
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Appointment updated successfully.")
        return response

    def get_success_url(self):
        return reverse("appointment-detail", args=[self.object.pk])


class AppointmentCancelView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status", "updated_at"])
        messages.success(request, "Appointment cancelled successfully.")
        return redirect("appointment-detail", pk=appointment.pk)
