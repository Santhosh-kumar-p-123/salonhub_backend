from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta, date,datetime

from .models import WorkingDay, Holiday, DailySlot

from .models import SlotMaster, WorkingDay, Holiday, DailySlot
from .serializers import (
    SlotMasterSerializer,
    WorkingDaySerializer,
    HolidaySerializer,
    DailySlotSerializer
)


class SlotMasterViewSet(viewsets.ModelViewSet):
    queryset = SlotMaster.objects.all().order_by("start_time")
    serializer_class = SlotMasterSerializer
    permission_classes = [permissions.IsAdminUser]


class WorkingDayViewSet(viewsets.ModelViewSet):
    queryset = WorkingDay.objects.all()
    serializer_class = WorkingDaySerializer
    permission_classes = [permissions.IsAdminUser]


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [permissions.IsAdminUser]


class DailySlotListAPIView(generics.ListAPIView):
    """
    USERS QUERY DAILY SLOTS HERE
    ?date=YYYY-MM-DD
    """
    serializer_class = DailySlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        date = self.request.query_params.get("date")
        if not date:
            return DailySlot.objects.none()

        # 1️⃣ Check if date is holiday
        if Holiday.objects.filter(holiday_date=date_obj).exists():
            return DailySlot.objects.none()  # No slots for holidays

        # 2️⃣ Return ONLY available slots
        return DailySlot.objects.filter(
            slot_date=date_obj,
            status="available",
            is_holiday=False
        ).select_related("slot_master").order_by("slot_master__start_time")

    def list(self, request, *args, **kwargs):
        date = request.query_params.get("date")

        # If holiday → send proper message
        if date and Holiday.objects.filter(holiday_date=date_obj).exists():
            return Response(
                {"message": "This date is a holiday — Booking not allowed."},
                status=400
            )

        return super().list(request, *args, **kwargs)


class AvailableDatesAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        today = date.today()

        available_dates = []

        # Check next 30 days
        for i in range(0, 30):
            current_date = today + timedelta(days=i)

            weekday = current_date.weekday()  # 0 = Monday ... 6 = Sunday

            # 1️⃣ Skip holiday
            if Holiday.objects.filter(holiday_date=current_date).exists():
                continue

            # 2️⃣ Skip non-working day
            if WorkingDay.objects.filter(weekday=weekday, is_working=False).exists():
                continue

            # 3️⃣ Must have at least 1 available slot for this date
            if DailySlot.objects.filter(
                slot_date=current_date,
                status="available",
                is_holiday=False
            ).exists():
                available_dates.append(str(current_date))

        return Response({"available_dates": available_dates})




