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
    serializer_class = DailySlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        date_str = self.request.query_params.get("date")

        if not date_str:
            return DailySlot.objects.none()

        # Convert param to date object
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return DailySlot.objects.none()

        # If holiday → no slots
        if Holiday.objects.filter(holiday_date=date_obj).exists():
            return DailySlot.objects.none()

        # Return available slots
        return DailySlot.objects.filter(
            slot_date=date_obj,
            status="available",
            is_holiday=False
        ).select_related("slot_master").order_by("slot_master__start_time")

    def list(self, request, *args, **kwargs):
        date_str = request.query_params.get("date")

        if not date_str:
            return Response({"message": "date parameter is required"}, status=400)

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return Response({"message": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        if Holiday.objects.filter(holiday_date=date_obj).exists():
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

        for i in range(0, 30):
            current_date = today + timedelta(days=i)
            weekday = current_date.weekday()  # 0 = Mon, 6 = Sun

            # 1️⃣ Skip holidays
            if Holiday.objects.filter(holiday_date=current_date).exists():
                continue

            # 2️⃣ Skip non-working days
            if WorkingDay.objects.filter(weekday=weekday, is_working=False).exists():
                continue

            # 3️⃣ Must have at least 1 available slot
            if DailySlot.objects.filter(
                slot_date=current_date,
                status="available",
                is_holiday=False
            ).exists():
                available_dates.append(str(current_date))

        # If no dates available
        if not available_dates:
            return Response({"available_dates": [], "message": "No available dates"}, status=200)

        return Response({"available_dates": available_dates}, status=200)





