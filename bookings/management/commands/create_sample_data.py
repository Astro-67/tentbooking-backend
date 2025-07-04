from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from bookings.models import TentType, Booking

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for tent booking system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating sample data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Booking.objects.all().delete()
            TentType.objects.all().delete()
            # Don't delete users to preserve admin accounts
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

        self.stdout.write('Creating sample tent types...')
        self.create_tent_types()
        
        self.stdout.write('Creating sample users...')
        self.create_sample_users()
        
        self.stdout.write('Creating sample bookings...')
        self.create_sample_bookings()
        
        self.stdout.write(self.style.SUCCESS('✅ Sample data created successfully!'))
        self.print_summary()

    def create_tent_types(self):
        tent_types_data = [
            {
                'name': 'Small Family Tent',
                'description': 'Perfect for small families or couples. Cozy and comfortable with basic amenities.',
                'capacity': 4,
                'price_per_day': Decimal('50.00'),
                'is_available': True
            },
            {
                'name': 'Medium Event Tent',
                'description': 'Ideal for medium-sized events, birthdays, and gatherings. Weather-resistant and spacious.',
                'capacity': 20,
                'price_per_day': Decimal('150.00'),
                'is_available': True
            },
            {
                'name': 'Large Wedding Tent',
                'description': 'Elegant tent perfect for weddings and large celebrations. Premium setup with decorative options.',
                'capacity': 50,
                'price_per_day': Decimal('300.00'),
                'is_available': True
            },
            {
                'name': 'Executive Conference Tent',
                'description': 'Professional setup for corporate events, conferences, and business meetings. Climate controlled.',
                'capacity': 30,
                'price_per_day': Decimal('250.00'),
                'is_available': True
            },
            {
                'name': 'Festival Mega Tent',
                'description': 'Massive tent for festivals, concerts, and large outdoor events. Sound system compatible.',
                'capacity': 100,
                'price_per_day': Decimal('500.00'),
                'is_available': True
            },
            {
                'name': 'Luxury Beach Tent',
                'description': 'Premium beachside tent with ocean views. Perfect for exclusive beach events and parties.',
                'capacity': 25,
                'price_per_day': Decimal('400.00'),
                'is_available': True
            },
            {
                'name': 'Adventure Camping Tent',
                'description': 'Rugged outdoor tent for camping adventures and survival experiences. Weatherproof.',
                'capacity': 8,
                'price_per_day': Decimal('80.00'),
                'is_available': True
            },
            {
                'name': 'Children\'s Party Tent',
                'description': 'Colorful and fun tent designed for children\'s parties and birthday celebrations.',
                'capacity': 15,
                'price_per_day': Decimal('120.00'),
                'is_available': True
            }
        ]

        for tent_data in tent_types_data:
            tent_type, created = TentType.objects.get_or_create(
                name=tent_data['name'],
                defaults=tent_data
            )
            if created:
                self.stdout.write(f'  ✓ Created: {tent_type.name}')
            else:
                self.stdout.write(f'  ○ Already exists: {tent_type.name}')

    def create_sample_users(self):
        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@tentbooking.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'phone_number': '+255123456789',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'  ✓ Created admin user: {admin_user.username}')
        else:
            self.stdout.write(f'  ○ Admin user already exists: {admin_user.username}')

        # Create sample customers
        customers_data = [
            {
                'username': 'john_doe',
                'email': 'john.doe@email.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+255987654321',
                'role': 'customer'
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@email.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone_number': '+255876543210',
                'role': 'customer'
            },
            {
                'username': 'ahmed_hassan',
                'email': 'ahmed.hassan@email.com',
                'first_name': 'Ahmed',
                'last_name': 'Hassan',
                'phone_number': '+255765432109',
                'role': 'customer'
            },
            {
                'username': 'fatima_ali',
                'email': 'fatima.ali@email.com',
                'first_name': 'Fatima',
                'last_name': 'Ali',
                'phone_number': '+255654321098',
                'role': 'customer'
            },
            {
                'username': 'david_johnson',
                'email': 'david.johnson@email.com',
                'first_name': 'David',
                'last_name': 'Johnson',
                'phone_number': '+255543210987',
                'role': 'customer'
            }
        ]

        for customer_data in customers_data:
            user, created = User.objects.get_or_create(
                username=customer_data['username'],
                defaults=customer_data
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  ✓ Created customer: {user.username}')
            else:
                self.stdout.write(f'  ○ Customer already exists: {user.username}')

    def create_sample_bookings(self):
        customers = User.objects.filter(role='customer')
        tent_types = TentType.objects.all()
        admin_user = User.objects.filter(role='admin').first()

        if not customers.exists() or not tent_types.exists():
            self.stdout.write(self.style.WARNING('No customers or tent types found. Skipping booking creation.'))
            return

        # Sample locations in Zanzibar
        locations = [
            'Stone Town Cultural Center',
            'Nungwi Beach Resort',
            'Kendwa Beach',
            'Paje Beach',
            'Jambiani Village',
            'Kizimkazi Fishing Village',
            'Forodhani Gardens',
            'Spice Farm Plantation',
            'Matemwe Beach',
            'Michamvi Peninsula'
        ]

        bookings_data = [
            {
                'customer': customers[0],
                'tent_type': tent_types[2],  # Large Wedding Tent
                'location': locations[0],
                'event_date': date.today() + timedelta(days=15),
                'end_date': date.today() + timedelta(days=16),
                'number_of_guests': 45,
                'special_requirements': 'Need sound system, decorative lighting, and catering setup area.',
                'status': 'confirmed'
            },
            {
                'customer': customers[1],
                'tent_type': tent_types[1],  # Medium Event Tent
                'location': locations[1],
                'event_date': date.today() + timedelta(days=7),
                'end_date': date.today() + timedelta(days=7),
                'number_of_guests': 18,
                'special_requirements': 'Beach setup required, wind-resistant installation.',
                'status': 'pending'
            },
            {
                'customer': customers[2],
                'tent_type': tent_types[5],  # Luxury Beach Tent
                'location': locations[2],
                'event_date': date.today() + timedelta(days=30),
                'end_date': date.today() + timedelta(days=32),
                'number_of_guests': 22,
                'special_requirements': 'VIP setup with premium furniture and bar area.',
                'status': 'confirmed'
            },
            {
                'customer': customers[3],
                'tent_type': tent_types[7],  # Children's Party Tent
                'location': locations[6],
                'event_date': date.today() + timedelta(days=5),
                'end_date': date.today() + timedelta(days=5),
                'number_of_guests': 12,
                'special_requirements': 'Colorful decorations, safe play area setup.',
                'status': 'pending'
            },
            {
                'customer': customers[4],
                'tent_type': tent_types[3],  # Executive Conference Tent
                'location': locations[7],
                'event_date': date.today() + timedelta(days=21),
                'end_date': date.today() + timedelta(days=23),
                'number_of_guests': 28,
                'special_requirements': 'Professional setup with projector, AC, and meeting furniture.',
                'status': 'confirmed'
            },
            {
                'customer': customers[0],
                'tent_type': tent_types[0],  # Small Family Tent
                'location': locations[8],
                'event_date': date.today() + timedelta(days=45),
                'end_date': date.today() + timedelta(days=47),
                'number_of_guests': 3,
                'special_requirements': 'Family camping setup with basic amenities.',
                'status': 'pending'
            },
            {
                'customer': customers[1],
                'tent_type': tent_types[4],  # Festival Mega Tent
                'location': locations[9],
                'event_date': date.today() + timedelta(days=60),
                'end_date': date.today() + timedelta(days=62),
                'number_of_guests': 85,
                'special_requirements': 'Large stage area, multiple entrances, food vendor spaces.',
                'status': 'pending'
            }
        ]

        for booking_data in bookings_data:
            booking = Booking(**booking_data)
            
            # Set confirmation details for confirmed bookings
            if booking.status == 'confirmed' and admin_user:
                booking.confirmed_by = admin_user
                booking.confirmed_at = timezone.now()
            
            booking.save()
            self.stdout.write(f'  ✓ Created booking: {booking}')

    def print_summary(self):
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📊 SAMPLE DATA SUMMARY'))
        self.stdout.write('='*50)
        
        tent_count = TentType.objects.count()
        user_count = User.objects.count()
        customer_count = User.objects.filter(role='customer').count()
        admin_count = User.objects.filter(role='admin').count()
        booking_count = Booking.objects.count()
        pending_bookings = Booking.objects.filter(status='pending').count()
        confirmed_bookings = Booking.objects.filter(status='confirmed').count()
        
        self.stdout.write(f'🏕️  Tent Types: {tent_count}')
        self.stdout.write(f'👥 Total Users: {user_count}')
        self.stdout.write(f'   - Customers: {customer_count}')
        self.stdout.write(f'   - Admins: {admin_count}')
        self.stdout.write(f'📅 Bookings: {booking_count}')
        self.stdout.write(f'   - Pending: {pending_bookings}')
        self.stdout.write(f'   - Confirmed: {confirmed_bookings}')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🚀 READY TO TEST!'))
        self.stdout.write('='*50)
        self.stdout.write('Login credentials for testing:')
        self.stdout.write('🔧 Admin: username=admin, password=admin123')
        self.stdout.write('👤 Customer: username=john_doe, password=password123')
        self.stdout.write('👤 Customer: username=jane_smith, password=password123')
        self.stdout.write('\n📖 API Documentation: http://localhost:8000/')
        self.stdout.write('⚙️  Admin Panel: http://localhost:8000/admin/')
        self.stdout.write('='*50)
