from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(View):
    """
    Simple health check endpoint to verify API is working
    """
    def get(self, request):
        return JsonResponse({
            'status': 'healthy',
            'message': '🏕️ Tent Booking API is running!',
            'version': '1.0.0',
            'endpoints': {
                'docs': '/',
                'admin': '/admin/',
                'auth': '/api/auth/',
                'tent_types': '/api/tent-types/',
                'bookings': '/api/bookings/',
            }
        })
