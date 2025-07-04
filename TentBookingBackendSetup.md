
# 🏕️ Tent Booking System Backend Setup Guide

This guide outlines step-by-step instructions to set up the Tent Booking System backend using Django and Django REST Framework, with JWT-based authentication and role-based access.

---

## 📦 Requirements

- Python 3.8+
- pip
- virtualenv
- PostgreSQL (or SQLite for development)

---

## 🚀 Step-by-Step Setup

### 1. Create and Activate Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 2. Install Dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary django-cors-headers
```

### 3. Start Django Project
```bash
django-admin startproject tentbooking
cd tentbooking
```

### 4. Create Django Apps
```bash
python manage.py startapp users
python manage.py startapp bookings
```

---

## 🧠 Project Structure (Basic)
```
tentbooking/
├── bookings/
├── users/
├── tentbooking/  # Main project settings
├── manage.py
```

---

## ⚙️ Configuration Steps

### 5. Add Apps and Middleware
In `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'users',
    'bookings',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True
```

### 6. Configure REST Framework & JWT
In `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

---

## 👥 Custom User Model with Roles

### 7. Create User Model in `users/models.py`
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
```

### 8. Set Custom User in Settings
```python
AUTH_USER_MODEL = 'users.User'
```

---

## 🔐 JWT Auth & Registration

### 9. Setup URLs for Authentication
In `tentbooking/urls.py`:
```python
from django.urls import path, include

urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('bookings.urls')),
]
```

### 10. Create User Views for Registration/Login
Implement JWT registration/login in `users/views.py` and add related URLs in `users/urls.py`

---

## 📅 Booking Functionality

### 11. Define Booking Model
In `bookings/models.py`:
```python
from django.db import models
from users.models import User

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    tent_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    event_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
```

### 12. Create Serializer and ViewSet for Booking
Create `serializers.py` and `views.py` inside `bookings/`.

---

## 🔄 Migrations & Superuser

### 13. Apply Migrations and Create Admin
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 🧪 Testing the API

Use tools like Postman or Swagger (optional) to test the API endpoints:
- `/api/token/` - login
- `/api/token/refresh/` - refresh token
- `/api/register/` - register
- `/api/bookings/` - create/view bookings

---

## ✅ MVP Check
- [x] User Registration/Login with JWT
- [x] Role-based access (admin/customer)
- [x] Create and view bookings
- [x] Admin can confirm bookings
- [x] CORS setup for frontend use

---

## 📦 Future Enhancements
- Tent type model
- Availability tracking
- Payment gateway integration
- Event calendar view for customers

---

## 📁 Ready for GitHub Copilot
Save this file as `README.md` and place it in your root backend folder. GitHub Copilot Pro will assist you in implementing each step effectively.

---

_Developed with 💡 to empower event organizers in Zanzibar._
