# Veterinary Clinic

A Django application for managing veterinary clinic clients, animals, and appointments.

## Features

- Dashboard with client and animal counts
- Daily and upcoming appointment overview
- Client search and profile management
- Animal records linked to clients
- Appointment creation, editing, filtering, and cancellation
- Appointment validation for client/animal ownership, positive duration, past dates, and overlapping bookings

## Requirements

- Python 3.10 or newer
- pip

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Apply database migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser.

## Verification

Run Django's system checks with:

```powershell
python manage.py check
```

The project uses SQLite for local development. The database file is intentionally excluded from version control, so run migrations after a fresh checkout.

## Main Routes

| Route | Purpose |
| --- | --- |
| `/` | Dashboard |
| `/clients/` | Browse and search clients |
| `/clients/new/` | Add a client |
| `/clients/<id>/` | View a client and their animals |
| `/appointments/` | Browse and filter appointments |

## Project Structure

```text
config/       Django settings, URL configuration, and WSGI entry point
clinic/       Clinic models, forms, views, templates, static files, and migrations
hello/        Small auxiliary Django app
manage.py     Django command-line entry point
requirements.txt
```

## Development Notes

This project is configured for local development with `DEBUG = True` and no authentication workflow. Do not deploy the default settings to production without adding production settings, authentication, secure secrets, and a production database configuration.
