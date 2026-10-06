from django.urls import path

from clinic.views import (
    AnimalCreateView,
    AnimalUpdateView,
    AppointmentCancelView,
    AppointmentCreateView,
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    ClientCreateView,
    ClientDetailView,
    ClientListView,
    ClientUpdateView,
    DashboardView,
)


urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("clients/", ClientListView.as_view(), name="client-list"),
    path("clients/new/", ClientCreateView.as_view(), name="client-create"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    path(
        "clients/<int:pk>/edit/",
        ClientUpdateView.as_view(),
        name="client-update",
    ),
    path(
        "clients/<int:client_pk>/animals/new/",
        AnimalCreateView.as_view(),
        name="animal-create",
    ),
    path(
        "clients/<int:client_pk>/animals/<int:pk>/edit/",
        AnimalUpdateView.as_view(),
        name="animal-update",
    ),
    path("appointments/", AppointmentListView.as_view(), name="appointment-list"),
    path(
        "clients/<int:client_pk>/appointments/new/",
        AppointmentCreateView.as_view(),
        name="appointment-create",
    ),
    path(
        "appointments/<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    path(
        "clients/<int:client_pk>/appointments/<int:pk>/edit/",
        AppointmentUpdateView.as_view(),
        name="appointment-update",
    ),
    path(
        "appointments/<int:pk>/cancel/",
        AppointmentCancelView.as_view(),
        name="appointment-cancel",
    ),
]