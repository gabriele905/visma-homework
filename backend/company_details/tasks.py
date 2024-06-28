from datetime import date, timedelta

from celery import shared_task

from backend.company_details.models import CompanyDetail


@shared_task(name='download_daily_data')
def download_daily_data():
    date_to = date.today()
    date_from = date_to - timedelta(days=1)

    for company in CompanyDetail.objects.all():
        company.download_data(date_from, date_to)
