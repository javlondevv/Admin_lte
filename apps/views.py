import os

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView

from apps.forms import BookingForm
from apps.models import Booking, Room, User


class BasePostView(View):
    """Parse reservation time, create reservation message, send message to Telegram, and create a booking entry in the database."""

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        room_id = request.POST.get("room_id")
        reservation_time = request.POST.get("reservationtime")

        check_in, check_out = self.parse_reservation_time(reservation_time)

        user = get_object_or_404(User, id=user_id)
        room = get_object_or_404(Room, id=room_id)

        message = self.create_reservation_message(user, room, check_in, check_out)

        self.send_message_to_telegram(message)

        self.create_booking(user, room, check_in, check_out)

        return HttpResponseRedirect("/")

    def parse_reservation_time(self, reservation_time):
        """Parse the reservation time into check-in and check-out timezone-aware datetime objects."""
        check_in_str, check_out_str = reservation_time.split(" - ")
        check_in = timezone.make_aware(
            timezone.datetime.strptime(check_in_str, "%m/%d/%Y %I:%M %p")
        )
        check_out = timezone.make_aware(
            timezone.datetime.strptime(check_out_str, "%m/%d/%Y %I:%M %p")
        )
        return check_in, check_out

    def create_reservation_message(self, user, room, check_in, check_out):
        """Create a formatted message for the reservation."""
        return (
            f"📝 *New Reservation*\n\n"
            f"👤 *Name*: {user.full_name} \n"
            f"📞 *Phone*: {user.phone} \n\n"
            f"✉️ *Room name*: {room.name}\n\n"
            f"✉️ *Type Room*: {room.room_type}\n\n"
            f"📅 *Check In*: {check_in.strftime('%m/%d/%Y %I:%M %p')}\n"
            f"📅 *Check Out*: {check_out.strftime('%m/%d/%Y %I:%M %p')}"
        )

    def send_message_to_telegram(self, message):
        """Send the reservation message to Telegram."""
        bot_token = os.environ.get("BOT_TOKEN")
        user_ids = os.environ.get("TELEGRAM_USER_IDS").split(" ")

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        for user_id in user_ids:
            payload = {"chat_id": user_id, "text": message, "parse_mode": "Markdown"}
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Request to Telegram API failed: {e}")

    def create_booking(self, user, room, check_in, check_out):
        """Create a booking entry in the database."""
        booking = Booking(user=user, room=room, check_in=check_in, check_out=check_out)
        booking.save()


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["rooms"] = Room.objects.order_by("-created_at")

        return context


class BookingView(BasePostView, ListView):
    model = Booking
    form_class = BookingForm
    template_name = "advanced.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["users"] = User.objects.filter(is_superuser=False).order_by("-date_joined")
        context["rooms"] = Room.objects.order_by("-created_at")

        selected_room_id = self.request.GET.get("room_id")
        context["selected_room"] = None

        if selected_room_id:
            try:
                context["selected_room"] = Room.objects.get(id=selected_room_id)
            except Room.DoesNotExist:
                context["selected_room"] = None

        return context
