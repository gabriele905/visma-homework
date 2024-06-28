from unittest.mock import patch

from django.test.client import RequestFactory

from backend.company_details.views import CompanyDetailList
from backend.helpers.tests import BaseTestCase, BaseMockFunctions
from backend.integrations.yahoo_finance import YahooFinanceClient


class CompanyDetailListTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company_meta = cls.create_company_detail('Meta', 'META')
        cls.company_netflix = cls.create_company_detail('Netflix', 'NFLX')
        cls.factory = RequestFactory()

    def test_get_queryset_gets_all(self):
        request = self.factory.get('/company_details')
        view = CompanyDetailList()
        view.setup(request)

        queryset = view.get_queryset()

        self.assertEqual(2, queryset.count())
        self.assertIn(self.company_meta, queryset)
        self.assertIn(self.company_netflix, queryset)

    def test_get_queryset_gets_by_symbol(self):
        request = self.factory.get(f'/company_details?symbol={self.company_netflix.symbol}')
        view = CompanyDetailList()
        view.setup(request)

        queryset = view.get_queryset()

        self.assertEqual(1, queryset.count())
        self.assertNotIn(self.company_meta, queryset)
        self.assertIn(self.company_netflix, queryset)

    def test_get_queryset_not_found_by_symbol(self):
        request = self.factory.get(f'/company_details?symbol={1}')
        view = CompanyDetailList()
        view.setup(request)

        queryset = view.get_queryset()

        self.assertEqual(0, queryset.count())


class CompanyDetailCreateTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company_meta = cls.create_company_detail('Meta', 'META')
        cls.factory = RequestFactory()

    def test_form_valid_symbol_already_exists(self):
        form_data = {
            'symbol': self.company_meta.symbol,
            'name': 'Netflix'
        }
        response = self.client.post('/company_details/new', form_data)

        self.assertEqual('Company detail with this Symbol already exists.',
                         response.context['form'].errors['symbol'][0])

    @patch.object(YahooFinanceClient, 'validate_ticker', new=BaseMockFunctions.mock_return_false)
    def test_form_valid_symbol_not_valid(self):
        form_data = {
            'symbol': 1,
            'name': 'Netflix'
        }
        response = self.client.post('/company_details/new', form_data)

        self.assertEqual('Symbol is not valid',
                         response.context['form'].errors['symbol'][0])

    @patch.object(YahooFinanceClient, 'validate_ticker', new=BaseMockFunctions.mock_return_true)
    def test_form_valid_symbol_not_valid(self):
        form_data = {
            'symbol': 'NFLX',
            'name': 'Netflix'
        }
        response = self.client.post('/company_details/new', form_data)

        self.assertRedirects(response, '/company_details/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class CompanyDetailUpdateTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company_meta = cls.create_company_detail('Meta', 'META')
        cls.company_netflix = cls.create_company_detail('Netflix', 'NFLX')
        cls.factory = RequestFactory()

    def test_form_valid_symbol_already_exists(self):
        form_data = {
            'symbol': self.company_netflix.symbol,
            'name': self.company_meta.name
        }
        response = self.client.post(f'/company_details/edit/{self.company_meta.id}', form_data)

        self.assertEqual('Company detail with this Symbol already exists.',
                         response.context['form'].errors['symbol'][0])

    @patch.object(YahooFinanceClient, 'validate_ticker', new=BaseMockFunctions.mock_return_false)
    def test_form_valid_symbol_not_valid(self):
        form_data = {
            'symbol': 1,
            'name': self.company_meta.name
        }
        response = self.client.post(f'/company_details/edit/{self.company_meta.id}', form_data)

        self.assertEqual('Symbol is not valid',
                         response.context['form'].errors['symbol'][0])

    @patch.object(YahooFinanceClient, 'validate_ticker', new=BaseMockFunctions.mock_return_true)
    def test_form_valid_symbol_not_valid(self):
        form_data = {
            'symbol': self.company_meta.name,
            'name': self.company_meta.name
        }
        response = self.client.post(f'/company_details/edit/{self.company_meta.id}', form_data)

        self.assertRedirects(response, '/company_details/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class CompanyDetailDeleteBySymbolTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company_meta = cls.create_company_detail('Meta', 'META')
        cls.factory = RequestFactory()

    def test_form_valid_symbol_is_required(self):
        form_data = {
            'symbol': '',
        }
        response = self.client.post('/company_details/delete_by_symbol', form_data)

        self.assertEqual('This field is required.', response.context['form'].errors['symbol'][0])

    def test_form_valid_company_not_found(self):
        form_data = {
            'symbol': '1',
        }
        response = self.client.post('/company_details/delete_by_symbol', form_data)

        self.assertEqual('Company not found', response.context['form'].errors['symbol'][0])

    def test_form_valid(self):
        form_data = {
            'symbol': self.company_meta.name,
        }
        response = self.client.post('/company_details/delete_by_symbol', form_data)

        self.assertRedirects(response, f'/company_details/delete/{self.company_meta.id}', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
