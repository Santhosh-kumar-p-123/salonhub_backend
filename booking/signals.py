# # booking/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Booking

# @receiver(post_save, sender=Booking)
# def notify_on_booking_change(sender, instance, created, **kwargs):
#     if created:
#         # Notify admins about new booking
#         admin_emails = []
#         try:
#             from django.contrib.auth import get_user_model
#             User = get_user_model()
#             admins = User.objects.filter(role__name__iexact='admin')
#             admin_emails = [u.email for u in admins if u.email]
#         except Exception:
#             admin_emails = [e[1] for e in getattr(settings, 'ADMINS', [])]

#         if admin_emails:
#             send_mail(
#                 'New booking created',
#                 f'Booking {instance.id} created by {instance.user.username}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 admin_emails,
#                 fail_silently=True
#             )
#     else:
#         # If booking updated to confirmed, notify the user
#         if instance.status == 'confirmed':
#             try:
#                 send_mail(
#                     f'Booking #{instance.id} confirmed',
#                     f'Hello {instance.user.username}, your booking #{instance.id} on {instance.start_slot.slot_date} has been confirmed.',
#                     settings.DEFAULT_FROM_EMAIL,
#                     [instance.user.email],
#                     fail_silently=True
#                 )
#             except Exception:
#                 pass
