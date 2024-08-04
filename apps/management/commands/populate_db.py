import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.models import User, Room


class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    ROOM_TYPES = [
        "Standard Double",
        "Standard Twin",
        "Superior Double",
        "Superior Twin",
        "Junior Suite Double",
        "Junior Suite Twin",
    ]

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create users
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password123',  # Use a common password
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_superuser=False,
                is_staff=True  # Set to True if you want them to access admin
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User {user.username} created'))

        # Create rooms
        for i in range(30):
            room_number = f"Room-{i + 1}"  # Create unique room numbers
            room_type = random.choice(self.ROOM_TYPES)
            room = Room.objects.create(
                room_number=room_number,
                room_type=room_type,
                description=fake.paragraph(),  # Random description
                price_per_night=round(random.uniform(50.0, 500.0), 2),  # Random price
                image=None,  # Set this to a valid image or keep it None
                is_available=random.choice([True, False])  # Random availability
            )
            room.save()
            self.stdout.write(self.style.SUCCESS(f'Room {room.room_number} created'))
