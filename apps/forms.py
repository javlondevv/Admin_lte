from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    check_in = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    check_out = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Booking
        fields = ["room", "check_in", "check_out"]
