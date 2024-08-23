import os
import django
import random
from faker import Faker
from api.models import User, Contact, SpamReport

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spam_checker.settings")
django.setup()

fake = Faker()

def populate_users(num_users=10):
    for _ in range(num_users):
        user = User.objects.create_user(
            username=fake.user_name(),
            phone_number=fake.phone_number(),
            password='password123'
        )
        for _ in range(5):
            Contact.objects.create(
                user=user,
                name=fake.name(),
                phone_number=fake.phone_number()
            )
        if random.choice([True, False]):
            SpamReport.objects.create(
                phone_number=user.phone_number,
                reported_by=user
            )

if __name__ == '__main__':
    populate_users()
