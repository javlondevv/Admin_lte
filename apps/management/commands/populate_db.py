import os
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker

from apps.models import User, Room

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        image_folder = 'media/images/'  # Path to your image folder
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]

        # Create users
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password123',
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_superuser=False,
                is_staff=True
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User {user.username} created'))

        # Create rooms
        existing_room_numbers = set(Room.objects.values_list('room_number', flat=True))
        existing_names = set(Room.objects.values_list('name', flat=True))  # Track existing names
        for i in range(30):
            room_number = f"Room-{i + 1}"
            # Ensure the room number is unique
            while room_number in existing_room_numbers:
                i += 1
                room_number = f"Room-{i + 1}"

            image_file_name = random.choice(image_files)

            # Open the image file
            image_path = os.path.join(image_folder, image_file_name)
            with open(image_path, 'rb') as img_file:
                image_content = ContentFile(img_file.read(), name=image_file_name)
                name = fake.catch_phrase()
                while name in existing_names:
                    name = fake.catch_phrase()
                room = Room.objects.create(
                    room_number=room_number,
                    name=name,
                    room_type=random.choice([
                        Room.STANDARD_DOUBLE,
                        Room.STANDARD_TWIN,
                        Room.SUPERIOR_DOUBLE,
                        Room.SUPERIOR_TWIN,
                        Room.JUNIOR_SUITE_DOUBLE,
                        Room.JUNIOR_SUITE_TWIN,
                    ]),
                    description=fake.paragraph(),
                    price_per_night=round(random.uniform(50.0, 500.0), 2),
                    image=image_content,
                    is_available=random.choice([True, False])
                )
                room.save()
                existing_room_numbers.add(room_number)  # Add to the existing room numbers
                self.stdout.write(self.style.SUCCESS(f'Room {room.room_number} created'))
