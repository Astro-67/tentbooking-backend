from django.contrib import admin
from django.utils import timezone
from .models import TentType, Booking


@admin.register(TentType)
class TentTypeAdmin(admin.ModelAdmin):
    """
    Admin configuration for TentType model
    """
    list_display = ('name', 'capacity', 'price_per_day', 'is_available', 'created_at')
    list_filter = ('is_available', 'capacity', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Booking model
    """
    list_display = (
        'id', 'customer', 'tent_type', 'location', 'event_date', 
        'status', 'total_amount', 'created_at'
    )
    list_filter = ('status', 'tent_type', 'event_date', 'created_at')
    search_fields = (
        'customer__username', 'customer__email', 'location', 
        'tent_type__name'
    )
    ordering = ('-created_at',)
    readonly_fields = ('total_amount', 'duration_days', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer',)
        }),
        ('Booking Details', {
            'fields': (
                'tent_type', 'location', 'event_date', 'end_date',
                'number_of_guests', 'special_requirements'
            )
        }),
        ('Status & Payment', {
            'fields': ('status', 'total_amount', 'duration_days')
        }),
        ('Confirmation Details', {
            'fields': ('confirmed_by', 'confirmed_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # If status is being changed to confirmed, set confirmation details
        if obj.status == 'confirmed' and not obj.confirmed_at:
            obj.confirmed_by = request.user
            obj.confirmed_at = timezone.now()
        super().save_model(request, obj, form, change)
