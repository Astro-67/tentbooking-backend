#!/bin/bash

echo "🏕️ Tent Booking System Setup"
echo "=============================="

# Navigate to the project directory
cd /home/astro/Tentbooking-Project/tentbooking-backend

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install missing dependencies
echo "Installing any missing dependencies..."
pip install -q drf-yasg inflection pytz pyyaml uritemplate packaging

# Run Django checks
echo "Running Django system checks..."
python manage.py check

# Create and apply migrations
echo "Creating migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

# Create sample data
echo "Setting up sample data..."
python setup_data.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the development server, run:"
echo "cd /home/astro/Tentbooking-Project/tentbooking-backend"
echo "source venv/bin/activate"
echo "python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
