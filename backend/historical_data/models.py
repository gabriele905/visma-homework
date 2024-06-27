from django.db import models


class HistoricalData(models.Model):
    company = models.ForeignKey('company_details.CompanyDetail', on_delete=models.CASCADE)
    date = models.DateField()
    open = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    close = models.IntegerField()
    adj_close = models.IntegerField()
    volume = models.IntegerField()

    def __str__(self):
        return self.date

    @staticmethod
    def get_csv_fields():
        return ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
