from django.urls import path

from apps.views import BookingView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("booking/", BookingView.as_view(), name="booking"),
]
