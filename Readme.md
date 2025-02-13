# SpamCheck API

A Django-based REST API for a spam-checking and contact lookup mobile application. This project uses a global database model to store all registered users, their contacts, and spam reports.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Data Population](#data-population)
- [Running the Project](#running-the-project)
- [API Contract](#api-contract)
- [Additional Notes](#additional-notes)
- [License](#license)

## Overview

This project implements a REST API with the following features:

- **User Registration & Login**: Users register with name, phone number, and optionally email; login returns an access token.
- **Global Database**: A `Global` model is used to store all searchable data (name, email, phone number, spam count).
- **Spam Reporting**: Users can mark a number as spam, which increments the spam count in the Global database.
- **Searching**: Users can search for a person by name or phone number. Results are ordered appropriately.
- **Detail View**: Clicking a search result returns full details, including email if conditions are met.
- **Caching & Rate Limiting**: Search results are cached for performance.

## Requirements

- Python 3.8+
- PostgreSQL
- Redis (for caching)
- Django
- Django REST Framework
- djangorestframework-simplejwt
- django-redis
- psycopg2-binary

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/spamcheck.git
cd spamcheck
```

### 2. Create a Virtual Environment and Activate It

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Database Configuration

Update `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spamcheck_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Cache Configuration

Ensure Redis is configured in `settings.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}
```

## Database Setup

### 1. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Data Population

To populate the database with sample data:

```bash
python manage.py populate_data
```

## Running the Project

Start the Django server:

```bash
python manage.py runserver
```

The API is now accessible at `http://localhost:8000/`.

## API Contract

### 1. User Registration

- **Endpoint:** `POST /api/register/`
- **Payload:**

```json
{
  "name": "John Doe",
  "phone_number": "1234567890",
  "email": "john@example.com",
  "password": "password123"
}
```

### 2. User Login

- **Endpoint:** `POST /api/login/`
- **Payload:**

```json
{
  "phone_number": "1234567890",
  "password": "password123"
}
```

### 3. Mark a Number as Spam

- **Endpoint:** `POST /api/spam/`
- **Payload:**

```json
{
  "phone_number": "9876543210"
}
```

### 4. Search by Name

- **Endpoint:** `GET /api/search/?name=Alice`
- **Response:**

```json
[
  {
    "id": 12,
    "name": "Alice Smith",
    "phone_number": "1112223333",
    "spam_likelihood": 1,
    "is_registered": true
  }
]
```

### 5. Search by Phone Number

- **Endpoint:** `GET /api/search/?phone=1234567890`
- **Response:**

```json
[
  {
    "id": 2,
    "name": "John Doe",
    "phone_number": "1234567890",
    "spam_likelihood": 0,
    "is_registered": true
  }
]
```

### 6. Get Contact Details

- **Endpoint:** `GET /api/contact/<contact_id>/`
- **Response:**

```json
{
  "id": 2,
  "name": "John Doe",
  "phone_number": "1234567890",
  "spam_likelihood": 1,
  "email": "john@example.com",
  "is_registered": true
}
```

## Additional Notes

- **Rate Limiting:** Configure middleware if needed.
- **Production Considerations:**
  - Set `DEBUG = False` in production.

## License

This project is provided as-is for demonstration purposes.

Happy Coding! 🚀
