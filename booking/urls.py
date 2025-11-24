# booking/urls.py
from django.urls import path
from .views import (
    CartAddView,
    CartView,
    CheckoutView,
    AdminAcceptView,
    AdminDeclineView,
    BookingHistoryView,
)

urlpatterns = [
    path('cart/add/<int:service_id>/', CartAddView.as_view()),
    path('cart/', CartView.as_view(), name='cart-view'),

    path('checkout/', CheckoutView.as_view(), name='booking-checkout'),

    # Admin endpoints
    path('admin/accept/', AdminAcceptView.as_view(), name='booking-admin-accept'),
    path('admin/decline/', AdminDeclineView.as_view(), name='booking-admin-decline'),

    path('history/', BookingHistoryView.as_view(), name='booking-history'),
]

