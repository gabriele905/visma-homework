from django.test import TestCase
from backend.company_details.models import CompanyDetail
from backend.historical_data.models import HistoricalData


class BaseTestCase(TestCase):
    @classmethod
    def create_company_detail(cls, name, symbol):
        return CompanyDetail.objects.create(
            name=name,
            symbol=symbol
        )

    @classmethod
    def create_historical_data(cls, company, date):
        return HistoricalData.objects.create(
            company=company,
            date=date,
            open=1,
            high=2,
            low=1,
            close=2,
            adj_close=2,
            volume=500
        )


class BaseMockFunctions:
    @staticmethod
    def mock_pass(*args, **kwargs):
        return None

    @staticmethod
    def mock_return_false(*args, **kwargs):
        return False

    @staticmethod
    def mock_return_true(*args, **kwargs):
        return True
