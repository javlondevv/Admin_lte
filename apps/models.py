from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db.models import (SET_NULL, BooleanField, CharField, DateTimeField,
                              DecimalField, ForeignKey, ImageField, Model,
                              TextField)
from django.utils import timezone

from apps.utils import generate_unique_filename


class CreatedBaseModel(Model):
    """
    Abstract base model with created and updated timestamps.
    """

    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class to mark this model as abstract.
        """

        abstract = True


class User(AbstractUser):
    """
    Represents a user with additional fields for phone number and date joined.

    Attributes:
        phone (str): The phone number of the user.
        date_joined (datetime): The date and time when the user joined.

    Properties:
        full_name (str): The full name of the user combining first name and last name.

    Methods:
        save(*args, **kwargs): Overrides the save method to set the username if not provided.
    """

    phone = CharField(max_length=15, blank=True, null=True)
    date_joined = DateTimeField(default=timezone.now)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.full_name
        super().save(*args, **kwargs)


class Room(CreatedBaseModel):
    """
    Model representing a room in a hotel.

    Attributes:
        room_number (str): The unique identifier for the room.
        room_type (str): The type of the room chosen from predefined choices.
        description (str): A description of the room.
        price_per_night (Decimal): The price per night for the room.
        image (ImageField): The image of the room.
        is_available (bool): Indicates if the room is available for booking.

    Methods:
        __str__(): Returns the room number as a string representation.
    """

    STANDARD_DOUBLE = "Standard Double"
    STANDARD_TWIN = "Standard Twin"
    SUPERIOR_DOUBLE = "Superior Double"
    SUPERIOR_TWIN = "Superior Twin"
    JUNIOR_SUITE_DOUBLE = "Junior Suite Double"
    JUNIOR_SUITE_TWIN = "Junior Suite Twin"

    ROOM_TYPE_CHOICES = [
        (STANDARD_DOUBLE, "Standard Double"),
        (STANDARD_TWIN, "Standard Twin"),
        (SUPERIOR_DOUBLE, "Superior Double"),
        (SUPERIOR_TWIN, "Superior Twin"),
        (JUNIOR_SUITE_DOUBLE, "Junior Suite Double"),
        (JUNIOR_SUITE_TWIN, "Junior Suite Twin"),
    ]
    room_number = CharField(max_length=10, unique=True)
    name = CharField(max_length=255,)
    room_type = CharField(
        max_length=50, choices=ROOM_TYPE_CHOICES, default=STANDARD_TWIN
    )
    description = TextField(blank=True, null=True)
    price_per_night = DecimalField(max_digits=10, decimal_places=2)
    image = ImageField(upload_to=generate_unique_filename)
    is_available = BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number}"


class Booking(CreatedBaseModel):
    """
    Model representing a booking for a room in a hotel.

    Attributes:
        user (User): The user who made the booking.
        room (Room): The room booked.
        check_in (datetime): The check-in date and time.
        check_out (datetime): The check-out date and time.
        total_price (Decimal): The total price for the booking.

    Methods:
        save(*args, **kwargs): Calculates the total price based on the duration of stay and room price per night.
    """

    user = ForeignKey("User", SET_NULL, "booked_rooms", null=True, blank=True)
    room = ForeignKey("Room", SET_NULL, "bookings", null=True, blank=True)
    check_in = DateTimeField()
    check_out = DateTimeField()
    total_price = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Booking by {self.user.full_name} for {self.room.room_number} from {self.check_in} to {self.check_out}"

    def save(self, *args, **kwargs):
        duration = Decimal((self.check_out - self.check_in).total_seconds() / 86400)
        self.total_price = duration * self.room.price_per_night
        super().save(*args, **kwargs)
