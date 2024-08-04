from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import ImageField
from django.utils.html import format_html

from . import utils
from .models import Booking, Room, User


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    """
    Customizes the admin interface for the Room model.

    Attributes:
        list_display (tuple): Specifies the fields to display in the admin list view.
        list_filter (tuple): Specifies the fields to use for filtering in the admin list view.
        search_fields (tuple): Specifies the fields to search for in the admin list view.
    """

    list_display = ("name", "room_number", "room_type", "price_per_night", "is_available", "display_image")
    list_filter = ("room_type", "is_available")
    search_fields = ("room_number",)
    formfield_overrides = {
        ImageField: {"widget": utils.ImagePreviewAdminWidget},
    }
    list_per_page = 5

    @staticmethod
    def display_image(obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" width="200" height="150" style="border-radius: 5px;">'
            )
        else:
            return "No image available"


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    """
    Customizes the admin interface for the Booking model.

    Attributes:
        list_display (tuple): Fields displayed in the admin list view.
        list_filter (tuple): Fields available for filtering in the admin list view.
        search_fields (tuple): Fields available for searching in the admin list view.
        readonly_fields (tuple): Fields that are read-only in the admin interface.

    Methods:
        get_user_full_name(obj): Returns the full name of the user associated with the booking.
        has_add_permission(request): Determines if the user has permission to add a new booking.
        has_change_permission(request, obj=None): Determines if the user has permission to change a booking.
        has_delete_permission(request, obj=None): Determines if the user has permission to delete a booking.
    """

    list_display = (
        "get_user_full_name",
        "room",
        "check_in",
        "check_out",
        "total_price",
        "created_at",
    )
    list_filter = ("check_in", "check_out")
    search_fields = ("user__username", "room__room_number", "room__hotel__name")
    readonly_fields = (
        "user",
        "room",
        "check_in",
        "check_out",
        "total_price",
        "created_at",
    )

    def get_user_full_name(self, obj):
        return obj.user.full_name

    get_user_full_name.short_description = "User Full Name"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(ModelAdmin):
    """
    Customizes the User admin interface with specific display, search, and exclusion settings.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields to enable search functionality in the admin.
        exclude (tuple): Fields to exclude from the admin interface.

    Methods:
        get_queryset(request): Filters the queryset to exclude superusers.
    """

    list_display = (
        "first_name",
        "last_name",
        "email",
    )
    search_fields = ("first_name", "email")
    exclude = (
        "last_login",
        "date_joined",
        "is_active",
        "is_staff",
        "password",
        "is_superuser",
        "groups",
        "user_permissions",
        "username",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_superuser=False)
