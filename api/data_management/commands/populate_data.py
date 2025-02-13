import random
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from api.models import Contact, Global

User = get_user_model()


class Command(BaseCommand):
    help = "Populate database with sample data using 10-digit phone numbers"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample registered users...")

        for i in range(10):
            phone_number = f"{random.randint(1000000000, 9999999999)}"
            name = f"User{i}"
            email = f"user{i}@example.com"

            # Ensure unique phone number
            if not User.objects.filter(phone_number=phone_number).exists():
                user = User.objects.create_user(
                    phone_number=phone_number,
                    name=name,
                    email=email,
                    password="password123",
                )

                # Ensure the user also exists in the Global table
                Global.objects.update_or_create(
                    phoneNumber=phone_number,
                    defaults={"name": name, "email": email, "spamCount": 0},
                )

        self.stdout.write("Registered users created and added to Global database.")

        # Fetch all users
        all_users = list(User.objects.all())

        self.stdout.write("Creating sample contacts...")
        sample_names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank"]

        for user in all_users:
            for _ in range(5):  # Each user gets 5 contacts
                contact_name = random.choice(sample_names) + get_random_string(3)
                contact_phone = f"{random.randint(1000000000, 9999999999)}"

                if not user.contacts.filter(phone_number=contact_phone).exists():
                    Contact.objects.create(
                        owner=user, name=contact_name, phone_number=contact_phone
                    )

                    # Ensure contacts exist in the Global database as well
                    Global.objects.update_or_create(
                        phoneNumber=contact_phone,
                        defaults={"name": contact_name, "email": None, "spamCount": 0},
                    )

        self.stdout.write("Contacts created and added to Global database.")

        self.stdout.write("Marking random numbers as spam...")

        spam_numbers = [f"{random.randint(1000000000, 9999999999)}" for _ in range(5)]

        for number in spam_numbers:
            global_entry, created = Global.objects.get_or_create(
                phoneNumber=number, defaults={"name": "", "email": None, "spamCount": 0}
            )

            # Randomly choose users to mark this number as spam
            spammers = random.sample(all_users, k=random.randint(1, len(all_users)))
            for _ in spammers:
                global_entry.spamCount += 1  # Increment spam count
            global_entry.save()

        self.stdout.write("Spam numbers updated in Global database.")

        self.stdout.write(self.style.SUCCESS("Database population complete."))
