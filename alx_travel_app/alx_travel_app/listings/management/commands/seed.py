from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        sample_locations = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru']

        for i in range(10):
            Listing.objects.create(
                name=f'Sample Listing {i+1}',
                description='This is a sample listing.',
                price_per_night=random.uniform(20.0, 100.0),
                location=random.choice(sample_locations)
            )

        self.stdout.write(self.style.SUCCESS('Database seeded with sample listings.'))
