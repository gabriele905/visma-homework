from datetime import date, timedelta
from unittest.mock import patch

from django.test.client import RequestFactory

from backend.company_details.models import CompanyDetail
from backend.helpers.tests import BaseTestCase, BaseMockFunctions
from backend.historical_data.views import HistoricalDataList


class CompanyDetailListTestCase(BaseTestCase):
    today = None
    yesterday = None
    tomorrow = None
    company = None

    @classmethod
    def setUpTestData(cls):
        cls.today = date.today()
        cls.yesterday = cls.today - timedelta(days=1)
        cls.tomorrow = cls.today + timedelta(days=1)

        cls.company = cls.create_company_detail('Netflix', 'NFLX')

        cls.historical_data_yesterday = cls.create_historical_data(cls.company, cls.yesterday)
        cls.historical_data_today = cls.create_historical_data(cls.company, cls.today)
        cls.historical_data_tomorrow = cls.create_historical_data(cls.company, cls.tomorrow)

        cls.factory = RequestFactory()

    def test_get_queryset_gets_all(self):
        request = self.factory.get(f'/historical_data/{self.company.id}')
        view = HistoricalDataList()
        view.setup(request, company_id=self.company.id)

        queryset = view.get_queryset()

        self.assertEqual(3, queryset.count())
        self.assertIn(self.historical_data_yesterday, queryset)
        self.assertIn(self.historical_data_today, queryset)
        self.assertIn(self.historical_data_tomorrow, queryset)

    def test_get_queryset_date_from_today(self):
        request = self.factory.get(f'/historical_data/{self.company.id}?date_from={self.today}')
        view = HistoricalDataList()
        view.setup(request, company_id=self.company.id)

        queryset = view.get_queryset()

        self.assertEqual(2, queryset.count())
        self.assertNotIn(self.historical_data_yesterday, queryset)
        self.assertIn(self.historical_data_today, queryset)
        self.assertIn(self.historical_data_tomorrow, queryset)

    def test_get_queryset_date_from_today_to_today(self):
        request = self.factory.get(f'/historical_data/{self.company.id}?date_from={self.today}&date_to={self.today}')
        view = HistoricalDataList()
        view.setup(request, company_id=self.company.id)

        queryset = view.get_queryset()

        self.assertEqual(1, queryset.count())
        self.assertNotIn(self.historical_data_yesterday, queryset)
        self.assertIn(self.historical_data_today, queryset)
        self.assertNotIn(self.historical_data_tomorrow, queryset)

    def test_get(self):
        response = self.client.get(
            f'/historical_data/{self.company.id}?date_from={self.today}&date_to={self.today}')

        self.assertEqual('text/html; charset=utf-8', response['content-type'])

    def test_get_csv(self):
        response = self.client.get(
            f'/historical_data/{self.company.id}?date_from={self.today}&date_to={self.today}&csv=1')

        self.assertEqual('text/csv', response['content-type'])


class HistoricalDataSyncTestCase(BaseTestCase):
    today = None

    @classmethod
    def setUpTestData(cls):
        cls.today = date.today()
        cls.yesterday = cls.today - timedelta(days=1)

        cls.company = cls.create_company_detail('Netflix', 'NFLX')

        cls.factory = RequestFactory()

    def test_form_valid_date_not_valid(self):
        form_data = {
            'date_from': self.today,
            'date_to': self.yesterday
        }
        response = self.client.post(f'/historical_data/{self.company.id}/sync', form_data)

        self.assertEqual('The "to" date must be later than the "from" date',
                         response.context['form'].errors['date_to'][0])

    def test_form_valid_company_not_found(self):
        form_data = {
            'date_from': self.yesterday,
            'date_to': self.today
        }
        response = self.client.post('/historical_data/999/sync', form_data)

        self.assertRedirects(response, '/company_details/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    @patch.object(CompanyDetail, 'download_data', new=BaseMockFunctions.mock_return_false)
    def test_form_valid_failed_to_download_data(self):
        form_data = {
            'date_from': self.yesterday,
            'date_to': self.today
        }
        response = self.client.post(f'/historical_data/{self.company.id}/sync', form_data)

        self.assertEqual('Failed to download data', response.context['form'].errors['__all__'][0])
