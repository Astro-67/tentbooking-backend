from rest_framework import serializers
from django.utils import timezone
from .models import Booking, TentType


class TentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for TentType model
    """
    class Meta:
        model = TentType
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new bookings
    """
    class Meta:
        model = Booking
        fields = (
            'tent_type', 'location', 'event_date', 'end_date', 
            'number_of_guests', 'special_requirements'
        )

    def validate(self, attrs):
        event_date = attrs.get('event_date')
        end_date = attrs.get('end_date')
        tent_type = attrs.get('tent_type')
        number_of_guests = attrs.get('number_of_guests')

        # Validate dates
        if event_date and event_date < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past.")
        
        if end_date and event_date and end_date < event_date:
            raise serializers.ValidationError("End date cannot be before event date.")
        
        # Validate capacity
        if tent_type and number_of_guests:
            if number_of_guests > tent_type.capacity:
                raise serializers.ValidationError(
                    f"Number of guests ({number_of_guests}) exceeds tent capacity ({tent_type.capacity})."
                )
        
        # Check tent availability
        if tent_type and not tent_type.is_available:
            raise serializers.ValidationError("Selected tent type is not available.")

        return attrs

    def create(self, validated_data):
        # Set customer to current user
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing bookings
    """
    tent_type_name = serializers.CharField(source='tent_type.name', read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    duration_days = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'customer_name', 'customer_username', 'tent_type_name',
            'location', 'event_date', 'end_date', 'duration_days',
            'number_of_guests', 'status', 'status_display', 'total_amount',
            'created_at', 'updated_at'
        )


class BookingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed booking view
    """
    tent_type = TentTypeSerializer(read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone_number', read_only=True)
    duration_days = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    confirmed_by_name = serializers.CharField(source='confirmed_by.get_full_name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


class BookingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating booking status (admin only)
    """
    class Meta:
        model = Booking
        fields = ('status', 'special_requirements')

    def update(self, instance, validated_data):
        user = self.context['request'].user
        
        # If status is being changed to confirmed, set confirmation details
        if validated_data.get('status') == 'confirmed' and instance.status != 'confirmed':
            if user.is_admin:
                instance.confirmed_by = user
                instance.confirmed_at = timezone.now()
            else:
                raise serializers.ValidationError("Only admins can confirm bookings.")
        
        return super().update(instance, validated_data)
