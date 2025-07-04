#!/usr/bin/env python
"""
Setup script to initialize the tent booking system with sample data
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append('/home/astro/Tentbooking-Project/tentbooking-backend')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tentbooking.settings')

# Initialize Django
django.setup()

from django.contrib.auth import get_user_model
from bookings.models import TentType
from decimal import Decimal

User = get_user_model()

def create_sample_data():
    """Create sample tent types and admin user"""
    
    print("🏕️ Setting up Tent Booking System...")
    
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@tentbooking.com',
            password='admin123',
            first_name='System',
            last_name='Administrator',
            role='admin'
        )
        print("✅ Admin user created: admin/admin123")
    else:
        print("ℹ️ Admin user already exists")
    
    # Create sample customer if it doesn't exist
    if not User.objects.filter(username='customer1').exists():
        customer_user = User.objects.create_user(
            username='customer1',
            email='customer@example.com',
            password='customer123',
            first_name='John',
            last_name='Doe',
            role='customer',
            phone_number='+255123456789'
        )
        print("✅ Sample customer created: customer1/customer123")
    else:
        print("ℹ️ Sample customer already exists")
    
    # Create sample tent types
    tent_types_data = [
        {
            'name': 'Standard Family Tent',
            'description': 'Perfect for family gatherings and small events. Comfortable seating for up to 50 people.',
            'capacity': 50,
            'price_per_day': Decimal('150.00')
        },
        {
            'name': 'Premium Wedding Tent',
            'description': 'Elegant tent perfect for weddings and formal events. Includes decorative lighting.',
            'capacity': 100,
            'price_per_day': Decimal('300.00')
        },
        {
            'name': 'Large Event Tent',
            'description': 'Spacious tent for large gatherings, corporate events, and festivals.',
            'capacity': 200,
            'price_per_day': Decimal('500.00')
        },
        {
            'name': 'Beach Party Tent',
            'description': 'Weather-resistant tent perfect for beach parties and outdoor celebrations.',
            'capacity': 75,
            'price_per_day': Decimal('200.00')
        }
    ]
    
    for tent_data in tent_types_data:
        if not TentType.objects.filter(name=tent_data['name']).exists():
            TentType.objects.create(**tent_data)
            print(f"✅ Created tent type: {tent_data['name']}")
        else:
            print(f"ℹ️ Tent type already exists: {tent_data['name']}")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📊 System Summary:")
    print(f"👥 Total Users: {User.objects.count()}")
    print(f"🏕️ Available Tent Types: {TentType.objects.count()}")
    print(f"📋 Total Bookings: {0}")  # No bookings initially
    
    print("\n🔗 API Endpoints:")
    print("📖 API Documentation: http://127.0.0.1:8000/")
    print("🔑 Admin Panel: http://127.0.0.1:8000/admin/")
    print("🔐 Login: POST /api/auth/login/")
    print("📝 Register: POST /api/auth/register/")
    print("🏕️ Tent Types: GET /api/tent-types/")
    print("📋 Bookings: GET /api/bookings/")

if __name__ == '__main__':
    create_sample_data()
