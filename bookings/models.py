from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class TentType(models.Model):
    """
    Model for different tent types available for booking
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(help_text="Maximum number of people")
    price_per_day = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"

    class Meta:
        verbose_name = "Tent Type"
        verbose_name_plural = "Tent Types"
        ordering = ['name']


class Booking(models.Model):
    """
    Model for tent bookings
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'customer'},
        related_name='bookings'
    )
    tent_type = models.ForeignKey(
        TentType,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    location = models.CharField(max_length=200)
    event_date = models.DateField()
    end_date = models.DateField()
    number_of_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    special_requirements = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'},
        related_name='confirmed_bookings'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username} - {self.tent_type.name}"

    @property
    def duration_days(self):
        return (self.end_date - self.event_date).days + 1

    def save(self, *args, **kwargs):
        # Calculate total amount based on tent type price and duration
        if self.tent_type and self.event_date and self.end_date:
            self.total_amount = self.tent_type.price_per_day * self.duration_days
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']
