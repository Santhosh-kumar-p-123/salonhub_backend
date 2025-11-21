# booking/serializers.py
from rest_framework import serializers
from .models import CartItem, Booking, BookingService
from services.models import Child_services
from scheduler.models import DailySlot

# ---------------------
# Cart Serializers (unchanged)
# ---------------------
class CartItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.child_service_name', read_only=True)
    price = serializers.DecimalField(source='service.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'service', 'service_name', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return float(obj.service.price) * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem  # note: if you have Cart model, adjust accordingly; user code used CartItem only
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        # if Cart model exists, implement accordingly. Placeholder:
        return 0


# ---------------------
# Booking / BookingService Serializers
# ---------------------
class BookingServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.child_service_name', read_only=True)

    class Meta:
        model = BookingService
        fields = ['id', 'service', 'service_name']


class BookingSerializer(serializers.ModelSerializer):
    booking_services = BookingServiceSerializer(source='services', many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    slot_info = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id', 'username', 'user', 'start_slot', 'slot_info',
            'booking_services', 'total_price', 'status', 'created_at', 'grand_total'
        ]
        read_only_fields = ['total_price', 'grand_total', 'status', 'created_at']

    def get_slot_info(self, obj):
        if not obj.start_slot:
            return None
        sm = obj.start_slot.slot_master
        return {
            "id": obj.start_slot.id,
            "date": obj.start_slot.slot_date,
            "start_time": sm.start_time,
            "end_time": sm.end_time,
            "status": obj.start_slot.status
        }


# ---------------------
# Create Booking Serializer (used by single endpoint)
# ---------------------
class CreateBookingSerializer(serializers.Serializer):
    start_slot_id = serializers.IntegerField()
    services = serializers.ListField(
        child=serializers.DictField(), allow_empty=False
    )

    def validate_start_slot_id(self, value):
        try:
            slot = DailySlot.objects.get(id=value)
        except DailySlot.DoesNotExist:
            raise serializers.ValidationError("Slot not found.")
        if slot.status != "available":
            raise serializers.ValidationError("Slot is not available.")
        return value

    def validate(self, data):
        # services must be list of { "service_id": <id> } or also include quantity if needed
        for s in data.get("services", []):
            service_id = s.get("service_id")
            if not service_id:
                raise serializers.ValidationError("Each service must include service_id.")
            if not Child_services.objects.filter(id=service_id).exists():
                raise serializers.ValidationError(f"Service {service_id} not found.")
        return data

    def create(self, validated_data):
        # NOTE: this create should be called inside a view that uses transaction.atomic() and select_for_update() on the slot
        user = self.context['request'].user
        slot = DailySlot.objects.get(id=validated_data['start_slot_id'])
        services = validated_data['services']

        booking = Booking.objects.create(user=user, start_slot=slot, status="pending")

        total = 0
        for item in services:
            service = Child_services.objects.get(id=item["service_id"])
            bs = BookingService.objects.create(
                booking=booking,
                service=service
            )
            total += float(service.price)

        # Update totals (gst_calculation uses model method)
        booking.calculate_totals()
        return booking
