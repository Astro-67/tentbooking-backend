from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Booking, TentType
from .serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
    BookingDetailSerializer,
    BookingUpdateSerializer,
    TentTypeSerializer
)


class TentTypeListView(generics.ListAPIView):
    """
    List all available tent types
    """
    queryset = TentType.objects.filter(is_available=True)
    serializer_class = TentTypeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="List all available tent types",
        responses={200: TentTypeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TentTypeDetailView(generics.RetrieveAPIView):
    """
    Get details of a specific tent type
    """
    queryset = TentType.objects.filter(is_available=True)
    serializer_class = TentTypeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Get tent type details",
        responses={200: TentTypeSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookingCreateView(generics.CreateAPIView):
    """
    Create a new booking
    """
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    @swagger_auto_schema(
        operation_description="Create a new booking",
        responses={
            201: BookingDetailSerializer,
            400: openapi.Response('Bad request')
        }
    )
    def post(self, request, *args, **kwargs):
        # Ensure only customers can create bookings
        if not request.user.is_customer:
            return Response(
                {'error': 'Only customers can create bookings.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response(
                BookingDetailSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(generics.ListAPIView):
    """
    List bookings based on user role
    """
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            # Admins can see all bookings
            return Booking.objects.all()
        else:
            # Customers can only see their own bookings
            return Booking.objects.filter(customer=user)

    @swagger_auto_schema(
        operation_description="List bookings (all for admin, own for customers)",
        responses={200: BookingListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookingDetailView(generics.RetrieveAPIView):
    """
    Get detailed view of a specific booking
    """
    serializer_class = BookingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(customer=user)

    @swagger_auto_schema(
        operation_description="Get booking details",
        responses={200: BookingDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookingUpdateView(generics.UpdateAPIView):
    """
    Update booking status (admin only) or customer details
    """
    serializer_class = BookingUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Booking.objects.all()
        else:
            # Customers can only update their pending bookings
            return Booking.objects.filter(customer=user, status='pending')

    @swagger_auto_schema(
        operation_description="Update booking (admin can change status, customers can update pending bookings)",
        responses={200: BookingDetailSerializer}
    )
    def put(self, request, *args, **kwargs):
        return self.update_booking(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update booking",
        responses={200: BookingDetailSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return self.update_booking(request, *args, **kwargs)

    def update_booking(self, request, *args, **kwargs):
        booking = self.get_object()
        
        # Check permissions for status updates
        if 'status' in request.data and not request.user.is_admin:
            return Response(
                {'error': 'Only admins can update booking status.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            updated_booking = serializer.save()
            return Response(
                BookingDetailSerializer(updated_booking).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Get booking statistics (admin only)",
    responses={200: openapi.Response('Booking statistics')}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_stats(request):
    """
    Get booking statistics (admin only)
    """
    if not request.user.is_admin:
        return Response(
            {'error': 'Permission denied. Admin access required.'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    stats = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_revenue': sum(
            booking.total_amount for booking in 
            Booking.objects.filter(status__in=['confirmed', 'completed'])
        )
    }
    
    return Response(stats, status=status.HTTP_200_OK)
