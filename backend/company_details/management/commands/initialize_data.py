from django.core.management.base import BaseCommand

from backend.company_details.models import CompanyDetail


class Command(BaseCommand):
    help = 'Initializes data from yahoo finance'

    def handle(self, *args, **options):
        obj, created = CompanyDetail.objects.update_or_create(
            name='Netflix, Inc.',
            symbol='NFLX'
        )

        if created:
            obj.download_data('2024-06-01', '2024-07-01')

        CompanyDetail.objects.update_or_create(
            name='Amazon.com, Inc.',
            symbol='AMZN'
        )

