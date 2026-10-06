# Veterinary Clinic Application: Technical Roadmap

## 1. Scope and Assumptions

This roadmap describes a small Django application for an interview exercise.

The initial product is a staff-facing veterinary clinic application. Clinic staff can create and manage clients, register their animals, and book appointments for them. Authentication and client self-service are future extensions rather than MVP requirements.

The MVP will use Django's server-rendered templates, SQLite, Django forms, Django's built-in generic views where appropriate, and the Django admin site for demonstration data.

## 2. Current Project Baseline

The repository currently contains:

- A minimal Django project named `config`.
- A single `hello` application.
- A placeholder home view that returns `Hello, world!`.
- SQLite configured as the database.
- Django 5.2 or newer, below version 6.0, specified in `requirements.txt`.
- One existing homepage test.

The initial `manage.py check` cannot currently run because Django is not installed in the active Python environment. Dependency installation is the first setup prerequisite.

## 3. Target Application Structure

Create a dedicated `clinic` application and gradually retire the placeholder `hello` workflow.

Expected structure:

```text
clinic/
    admin.py
    apps.py
    forms.py
    migrations/
    models.py
    tests/
        __init__.py
        test_models.py
        test_clients.py
        test_animals.py
        test_appointments.py
    urls.py
    views.py
    templates/
        clinic/
            base.html
            dashboard.html
            clients/
            animals/
            appointments/
```

The project-level URL configuration will include `clinic.urls`.

## 4. Domain Model Plan

### Client

Fields:

- `name`
- `email`
- `phone`
- `address`
- `notes`
- `created_at`
- `updated_at`

A client can own multiple animals and have multiple appointments.

### Animal

Fields:

- `client` foreign key
- `name`
- `species`
- `breed`
- `date_of_birth`
- `notes`
- `created_at`
- `updated_at`

Every animal belongs to exactly one client. Animal management should be initiated from a client context so ownership cannot be assigned accidentally.

### Appointment

Fields:

- `client` foreign key
- `animal` foreign key
- `scheduled_for`
- `reason`
- `status`
- `notes`
- `created_at`
- `updated_at`

Recommended statuses:

- `scheduled`
- `completed`
- `cancelled`

The selected animal must belong to the selected client. Scheduled appointments for the same animal must not overlap. Cancelled appointments do not block a new booking.

## 5. Implementation Milestones

### Milestone 1: Project Setup

- Install dependencies from `requirements.txt`.
- Create and register the `clinic` app.
- Configure templates and static files.
- Add a shared base template and basic navigation.
- Replace the placeholder homepage with a clinic dashboard.
- Confirm `python manage.py check` passes.

### Milestone 2: Models and Database

- Implement `Client`, `Animal`, and `Appointment` models.
- Add model metadata, useful string representations, and indexes where useful.
- Create and apply migrations.
- Register all models in Django admin.
- Add model-level tests for relationships and constraints.

### Milestone 3: Client Management

Routes:

- `GET /clients/` - list clients.
- `GET /clients/new/` and `POST /clients/new/` - create a client.
- `GET /clients/<id>/` - view client details.
- `GET /clients/<id>/edit/` and `POST /clients/<id>/edit/` - update a client.

Features:

- Required-field validation.
- Email validation.
- Search by name, email, or phone.
- Links to the client's animals and appointments.
- Success messages after create and update operations.

### Milestone 4: Animal Management

- Add an animal from a client detail page.
- Edit an animal.
- Display all animals belonging to a client.
- Display animal details and appointment history.
- Ensure the animal's client relationship cannot be changed accidentally through the form.

### Milestone 5: Appointment Booking

- Add an appointment from a client or animal page.
- List appointments.
- View appointment details.
- Edit an appointment.
- Cancel an appointment.

Validation:

- Appointment date and time cannot be in the past for a new booking.
- Animal must belong to the selected client.
- Scheduled appointments for the same animal cannot overlap.
- Cancelled appointments do not prevent rebooking.
- Status is visible and changes are controlled.

### Milestone 6: User Experience and Error Handling

- Add consistent navigation between clients, animals, and appointments.
- Show validation errors beside relevant fields.
- Use Django messages for successful operations.
- Add empty states for lists with no data.
- Add confirmation for appointment cancellation.
- Return useful 404 responses for missing clients, animals, and appointments.

### Milestone 7: Quality and Cleanup

- Run the complete test suite.
- Remove or replace the placeholder `hello` test.
- Run Django system checks.
- Review migrations and admin usability.
- Verify the primary workflows manually in a browser.
- Document local setup and test commands.

## 6. Test-First Acceptance Coverage

Implement each milestone using red, green, and refactor steps.

Required tests:

- A client can be created, listed, viewed, and updated.
- Invalid client email input is rejected.
- An animal is associated with the correct client.
- An animal cannot be assigned to another client through an appointment form.
- An appointment requires a valid client and animal relationship.
- Past appointment bookings are rejected.
- Overlapping appointments for one animal are rejected.
- Cancelled appointments allow a new booking in the same time slot.
- Main pages return successful HTTP responses.
- Successful form submissions redirect to the expected detail or list page.
- Missing records return HTTP 404 responses.

## 7. URL and View Design

Use Django forms for input validation and generic class-based views where they keep the implementation clear. Keep domain-specific appointment conflict validation in a reusable form or model/service boundary rather than duplicating it across views.

The initial URL groups should be:

```text
/                       dashboard
/clients/               client list
/clients/new/           create client
/clients/<id>/          client detail
/clients/<id>/edit/     update client
/clients/<id>/animals/new/  add animal
/animals/<id>/edit/     update animal
/appointments/          appointment list
/appointments/new/      book appointment
/appointments/<id>/     appointment detail
/appointments/<id>/edit/   update appointment
/appointments/<id>/cancel/ cancel appointment
```

## 8. Security and Data Integrity

- Keep CSRF protection enabled.
- Use Django forms rather than trusting raw POST data.
- Scope child-object lookups to their parent where applicable.
- Use database transactions for booking operations if the implementation performs multiple writes.
- Add database constraints where they can express the business rule reliably.
- Do not add authentication until the staff-facing MVP is working and tested.

## 9. Future Extensions

These are explicitly outside the first implementation slice:

- Client accounts and login.
- Client-facing appointment requests.
- Vet and staff roles with permissions.
- Multiple clinic locations.
- Appointment reminders.
- Vaccination and medical records.
- JSON API or REST framework integration.
- PostgreSQL deployment configuration.

## 10. Recommended First Coding Slice

Begin with:

1. Install Django dependencies.
2. Create and register the `clinic` app.
3. Implement the three models.
4. Add migrations and admin registration.
5. Write model tests for ownership and appointment conflict rules.
6. Run the focused tests before building the user interface.
