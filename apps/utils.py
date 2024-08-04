import uuid

from django.forms import FileInput
from django.utils.html import format_html


def generate_unique_filename(instance, filename):
    extension = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    return f"images/{unique_filename}"


class ImagePreviewAdminWidget(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            image_html = format_html(
                '<img src="{}"style=" border:1px solid #00000040; border-radius:5px; max-width:300px; max-height:300px;" />',
                value.url,
            )
            output.append(image_html)
        output.append(super().render(name, value, attrs, renderer))
        return format_html("".join(output))


class VideoPreviewAdminWidget(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            video_html = format_html(
                '<video width="320" height="240" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                value.url,
            )
            output.append(video_html)
        output.append(super().render(name, value, attrs, renderer))
        return format_html("".join(output))
