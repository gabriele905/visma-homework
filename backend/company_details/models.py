from django.db import models
from django.urls import reverse

from backend.integrations.yahoo_finance import YahooFinanceClient

from backend.historical_data.models import HistoricalData


class CompanyDetail(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_detail_edit', kwargs={'pk': self.pk})

    def download_data(self, date_from, date_to):
        yf_client = YahooFinanceClient(self.symbol)

        data = yf_client.historical_data(date_from, date_to)

        if data.empty:
            return

        for index, row in data.iterrows():
            defaults = {
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'adj_close': row['Adj Close'],
                'volume': row['Volume'],
            }
            HistoricalData.objects.update_or_create(
                company=self, date=index.strftime('%Y-%m-%d'),
                defaults=defaults
            )

        return True
