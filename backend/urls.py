from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenRefreshView


def home(request):
    return JsonResponse({
        "message": "Welcome to SalonHub API",
        "available_endpoints": [
            "/api/auth/",
            "/api/services/",
            "/api/scheduler/",
            "/api/booking/",
            "/admin/"
        ]
    })

urlpatterns = [
    path('', home),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/services/', include('services.urls')),
    path('api/scheduler/', include('scheduler.urls')),
    path('api/booking/', include('booking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

