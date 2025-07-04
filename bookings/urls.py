from django.urls import path
from .views import (
    TentTypeListView,
    TentTypeDetailView,
    BookingCreateView,
    BookingListView,
    BookingDetailView,
    BookingUpdateView,
    booking_stats,
)

app_name = 'bookings'

urlpatterns = [
    # Tent type endpoints
    path('tent-types/', TentTypeListView.as_view(), name='tent_type_list'),
    path('tent-types/<int:pk>/', TentTypeDetailView.as_view(), name='tent_type_detail'),
    
    # Booking endpoints
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    
    # Statistics endpoint (admin only)
    path('bookings/stats/', booking_stats, name='booking_stats'),
]
