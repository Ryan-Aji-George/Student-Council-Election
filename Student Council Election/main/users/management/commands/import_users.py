from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
import pandas as pd
import random
import sys
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Import users from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def generate_unique_random_username(self):
        """Generate a random 5-digit username that doesn't exist in the database."""
        while True:
            random_num = random.randint(10000, 99999)
            username = f"{random_num:05d}"
            if not User.objects.filter(username=username).exists():
                return username

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading Excel file: {e}"))
            return

        valid_houses = [choice[0] for choice in Profile.HOUSE_CHOICES]
        total_rows = len(df)
        self.stdout.write(self.style.NOTICE(f"Importing {total_rows} users…"))

        # Initialize a permanent in-place progress bar at the bottom (position=1)
        pbar = tqdm(
            df.iterrows(),
            total=total_rows,
            desc="Importing users",
            unit="row",
            file=sys.stdout,
            leave=True,
            dynamic_ncols=True,
            position=1
        )

        for index, row in pbar:
            # Skip rows with missing full names
            if pd.isna(row.get('Full Name', None)):
                tqdm.write(self.style.WARNING(f"Skipping row {index}: missing Full Name"), file=sys.stdout)
                continue

            # Generate credentials
            username = self.generate_unique_random_username()
            user = User.objects.create_user(username=username, password=username)
            profile = user.profile

            # Populate profile fields
            profile.voter_name = str(row['Full Name']).strip()

            house = str(row.get('House', '')).strip().title() if not pd.isna(row.get('House', None)) else 'None'
            profile.house = house if house in valid_houses else 'None'
            if house not in valid_houses and house != 'None':
                tqdm.write(self.style.WARNING(f"Invalid house '{house}' for user {username}, set to 'None'"), file=sys.stdout)

            voter_class = (
                str(row.get('Class', '')).strip().upper().replace(" ", "")
                if not pd.isna(row.get('Class', None)) else ''
            )
            profile.voter_class = voter_class
            profile.save()

            # Print a success message above the bar
            tqdm.write(
                self.style.SUCCESS(
                    f"Profile for {profile.voter_name} created (ID {username}, house {profile.house}, class {profile.voter_class})"
                ),
                file=sys.stdout
            )

        pbar.close()

        # Final success message after the loop
        self.stdout.write(self.style.SUCCESS('''


░██████╗██╗░░░██╗░█████╗░░█████╗░███████╗░██████╗░██████╗███████╗██╗░░░██╗██╗░░░░░██╗░░░░░██╗░░░██╗
██╔════╝██║░░░██║██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝██║░░░██║██║░░░░░██║░░░░░╚██╗░██╔╝
╚█████╗░██║░░░██║██║░░╚═╝██║░░╚═╝█████╗░░╚█████╗░╚█████╗░█████╗░░██║░░░██║██║░░░░░██║░░░░░░╚████╔╝░
░╚═══██╗██║░░░██║██║░░██╗██║░░██╗██╔══╝░░░╚═══██╗░╚═══██╗██╔══╝░░██║░░░██║██║░░░░░██║░░░░░░░╚██╔╝░░
██████╔╝╚██████╔╝╚█████╔╝╚█████╔╝███████╗██████╔╝██████╔╝██║░░░░░╚██████╔╝███████╗███████╗░░░██║░░░
╚═════╝░░╚═════╝░░╚════╝░░╚════╝░╚══════╝╚═════╝░╚═════╝░╚═╝░░░░░░╚═════╝░╚══════╝╚══════╝░░░╚═╝░░░

██╗███╗░░░███╗██████╗░░█████╗░██████╗░████████╗███████╗██████╗░
██║████╗░████║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║██╔████╔██║██████╔╝██║░░██║██████╔╝░░░██║░░░█████╗░░██║░░██║
██║██║╚██╔╝██║██╔═══╝░██║░░██║██╔══██╗░░░██║░░░██╔══╝░░██║░░██║
██║██║░╚═╝░██║██║░░░░░╚█████╔╝██║░░██║░░░██║░░░███████╗██████╔╝
╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░

██╗░░░██╗░██████╗███████╗██████╗░░██████╗  ██╗
██║░░░██║██╔════╝██╔════╝██╔══██╗██╔════╝  ██║
██║░░░██║╚█████╗░█████╗░░██████╔╝╚█████╗░  ██║
██║░░░██║░╚═══██╗██╔══╝░░██╔══██╗░╚═══██╗  ╚═╝
╚██████╔╝██████╔╝███████╗██║░░██║██████╔╝  ██╗
░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░  ╚═╝

'''))