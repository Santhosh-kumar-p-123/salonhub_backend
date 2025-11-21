# booking/management/commands/expire_pending_bookings.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from booking.models import Booking, RESERVATION_MINUTES
from scheduler.models import DailySlot

class Command(BaseCommand):
    help = "Expire pending bookings older than RESERVATION_MINUTES and free their slots"

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(minutes=RESERVATION_MINUTES)
        expired = Booking.objects.filter(status='pending', created_at__lt=cutoff)
        count = expired.count()
        for b in expired:
            # free related slots (booking.start_slot and possibly more if compute_required_slot_master_ids used)
            start = b.start_slot
            # free only the start slot to be safe, or free related slots if you track them elsewhere
            if start:
                start.status = 'available'
                start.booked_by = None
                start.booked_service = None
                start.save()
            b.status = 'cancelled'
            b.save(update_fields=['status'])
        self.stdout.write(self.style.SUCCESS(f"Expired {count} pending bookings"))
